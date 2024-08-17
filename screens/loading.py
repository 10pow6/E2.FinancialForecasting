from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import LoadingIndicator, RichLog, Header, Footer
from textual.worker import Worker
import json
from statics import DirectoryConfig
import datetime
import timeit
from helpers import spend_worker

from concurrent.futures import ProcessPoolExecutor
import asyncio

class Loading(Screen):
    def __init__(self, init_mode: str, init_msg: str, api_handler, snapshot_name=None) -> None:
        self.init_mode = init_mode
        self.init_msg = init_msg
        self.api_handler = api_handler
        self.tile_info = {}
        self.final_calc = []
        self.snapshot_name=snapshot_name

        # need to update this logic so it makes sense... keep in my we may load old snapshots.  need some naming format that captures the load =p. 
        # probably calculated.snapshot-timestamp.json that cooresponds to either the thing we LOADED or the thing we generated.  
        # right now end to end maps.  this will break naming convention wise on load
        # probably if we are in "load mode", just overwrite this with the parsed out timestamp
        now = datetime.datetime.now()
        self.formatted_datetime = now.strftime("%Y%m%d%H%M%S")

        # override to match the loaded snapshot ;).  format is always the same from this app
        if self.init_mode == "flow.push.load_snapshot":
            self.formatted_datetime=self.snapshot_name[9:-5]
        

        self.start = timeit.default_timer()
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        yield LoadingIndicator()
        yield RichLog(highlight=True, markup=True)
        yield Footer()
    
    async def call_apis(self):
        text_log = self.query_one(RichLog)
        text_log.write("Starting API pull of T1 & T2 Data.")
        text_log.write("Starting API pull of T3 Data (this can take a little).")
        # API Pulls
        workers=[self.run_worker(self.api_handler.tileprices_v2(), exclusive=False),
                 self.run_worker(self.api_handler.territory_prices(), exclusive=False)]
        await self.workers.wait_for_complete(workers)
        return True

    async def process_spend(self, MAX_WORKERS=8):
        executor = ProcessPoolExecutor(max_workers=MAX_WORKERS)


        country_data = self.tile_info["countries"]
        territory_data = self.tile_info["territories"]
        text_log = self.query_one(RichLog)
        text_log.write("Starting user spend calculation for T1 & T2 (this can take a little).")

        loop = asyncio.get_running_loop()

        # Process countries (T1 & T2)
        country_futures = []
        for country in country_data:
            if country["landfield_tier"] != 3:
                future = loop.run_in_executor(
                    executor,
                    spend_worker,
                    country["totalTilesSold"],
                    country["value"],
                    country["landfield_tier"],
                    country["countryCode"]
                )
                country_futures.append(future)
        
        country_results = await asyncio.gather(*country_futures)
        self.final_calc.extend(country_results)
        
        text_log.write("Completed processing T1 & T2.")
        text_log.write("Starting user spend calculation for T3 (this can take a little).")

        # Process territories (T3)
        territory_futures = []
        for territory in territory_data:
            future = loop.run_in_executor(
                executor,
                spend_worker,
                territory["estimatedTilesSold"],
                territory["estimatedValue"],
                3,
                territory["id"]
            )
            territory_futures.append(future)
        
        territory_results = await asyncio.gather(*territory_futures)
        self.final_calc.extend(territory_results)

        text_log.write("Completed processing T3.")
        executor.shutdown(wait=True)


        path = DirectoryConfig.calculated
        filename = f"calculated.snapshot-{self.formatted_datetime}.json"

        with open(path+"/"+filename, 'w') as file:
            json.dump(self.final_calc, file, indent=4)

        text_log = self.query_one(RichLog)
        text_log.write("Successfully wrote calculated file.")
        
        return True    
    
    def on_mount(self) -> None:
        LOAD_MODE = (self.init_mode == "flow.push.load_snapshot")

        text_log = self.query_one(RichLog)
        text_log.write("[bold magenta]"+self.init_msg)

        if( not LOAD_MODE ):
            self.run_worker(self.call_apis(), exclusive=False)
        elif( LOAD_MODE ):
            text_log.write("Processing user spend.")
            path = DirectoryConfig.snapshots
            snapshot=self.snapshot_name
            with open(path+"/"+snapshot, 'r') as file:
                self.tile_info = json.load(file)
            self.run_worker(self.process_spend(), exclusive=False)
        
    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
            """Called when the worker state changes."""
            if( event.worker.name=="tileprices_v2" and event.worker.result != None):
                self.log(event)
                self.log(event.worker.result)
                
                self.tile_info["countries"] = event.worker.result

                text_log = self.query_one(RichLog)
                text_log.write("Pulled data from tile statistics (valid for T1 & T2).")
            elif( event.worker.name=="territory_prices" and event.worker.result != None):
                self.log(event)
                self.log(event.worker.result)
                
                self.tile_info["territories"] = event.worker.result

                text_log = self.query_one(RichLog)
                text_log.write("Pulled data from tile statistics (Territories).")
            elif( event.worker.name=="process_spend" and event.worker.result != None):
                text_log = self.query_one(RichLog)
                total=0
                for entry in self.final_calc:
                    total+=entry["userSpend"]
                text_log.write(f"Total: {total}")
                stop = timeit.default_timer()
                text_log.write(f'Complete. Processing Time: {stop - self.start}')  
            elif( event.worker.name=="call_apis" and event.worker.result != None):
                #country_data = self.tile_info["countries"]
                #territory_data = self.tile_info["territories"]
                # Write Snapshot after API calls
                path = DirectoryConfig.snapshots
                
                filename = f"snapshot-{self.formatted_datetime}.json"
                self.snapshot_name=filename

                with open(path+"/"+filename, 'w') as file:
                    json.dump(self.tile_info, file, indent=4)

                text_log = self.query_one(RichLog)
                text_log.write("Successfully wrote snapshot file.")

                text_log.write("Processing user spend.")
                self.run_worker(self.process_spend(), exclusive=False)

                