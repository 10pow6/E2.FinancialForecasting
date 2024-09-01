from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static,Tabs,Tab, Label
import numpy as np

class Report(Screen):   
    def __init__(self, init_msg:str, final_calc:dict, aggregates:dict, forecasting_config:dict) -> None:
        self.init_msg = init_msg
        self.final_calc = final_calc
        self.aggregates = aggregates
        self.forecasting_config = forecasting_config
        self.tabs = [Tab("FULL",id="FULL")]

        self.project_data={}
        self.projections={}

        self.calculations = {}
        for year_key, year_data in forecasting_config["DYNAMIC"].items():
            self.tabs.append(Tab(year_key,id=year_key))

            # allocation to the year
            year_allocation=self.aggregates["total_spend"] * year_data["TOTAL_TILE_SALE_ALLOCATION_PERC"]

            year_rev_fees=year_allocation * forecasting_config["FLAT"]["REV_FEES"]
            year_rev_interest=year_allocation * forecasting_config["FLAT"]["REV_INTEREST"]
            year_rev_skins=year_data["REV_SKINS"]
            year_rev_other=year_data["REV_OTHER"]
            year_rev_holobuilding=year_data["REV_HOLOBUILDING"]
            
            
            year_exp_fraud=year_allocation * year_data["EXP_FRAUD"]
            year_exp_bugs=year_allocation * year_data["EXP_BUGS"]
            year_exp_taxes=year_allocation * forecasting_config["FLAT"]["EXP_TAXES"]
            year_exp_lit=year_allocation * forecasting_config["FLAT"]["EXP_LIT"]
            year_exp_ref=year_allocation * forecasting_config["FLAT"]["EXP_REF"]
            year_exp_operational=year_data["EXP_OPERATIONAL"]
            year_exp_tile_upgrades=year_data["EXP_TILE_UPGRADES"]
            year_exp_salaries=year_data["EXP_SALARIES"]
            year_exp_acquisitions=year_data["EXP_ACQUISITIONS"]
            year_exp_other=year_data["EXP_OTHER"]
            

            #healt calc
            health=(year_allocation
            + year_rev_skins
            + year_rev_fees
            + year_rev_interest
            + year_rev_other
            + year_rev_holobuilding
            - year_exp_fraud
            - year_exp_bugs
            - year_exp_taxes
            - year_exp_salaries
            - year_exp_operational
            - year_exp_acquisitions
            - year_exp_tile_upgrades
            - year_exp_lit
            - year_exp_ref
            - year_exp_other
            )

            projection_data = {
                "allocation": year_allocation,
                "rev_skins": year_rev_skins,
                "rev_fees": year_rev_fees,
                "rev_other": year_rev_other,
                "rev_holobuilding": year_rev_holobuilding,
                "rev_interest": year_rev_interest,
                "exp_fraud": year_exp_fraud,
                "exp_bugs": year_exp_bugs,
                "exp_taxes": year_exp_taxes,
                "exp_salaries": year_exp_salaries,
                "exp_operational": year_exp_operational,
                "exp_acquisitions": year_exp_acquisitions,
                "exp_tile_upgrades": year_exp_tile_upgrades,
                "exp_lit": year_exp_lit,
                "exp_ref": year_exp_ref,
                "exp_other":year_exp_other,
                "health": health
            }
            projection_text = self.create_projection_text(projection_data)

            self.projections[year_key] = {
                "data":projection_data,
                "text":projection_text
            }

            
        # Calculate the sum of all projections for the FULL view
        full_projection = {key: sum(year['data'][key] for year in self.projections.values()) for key in self.projections[list(self.projections.keys())[0]]['data']}
        self.projections["FULL"] = {
            "data": full_projection,
            "text": self.create_projection_text(full_projection)
        }

        super().__init__()

    def create_projection_text(self, data):
        return f"""
            (+) Player spend on tiles: {self.format_currency(data['allocation'])}
            (+) Skin Sales: {self.format_currency(data['rev_skins'])}
            (+) Fees: {self.format_currency(data['rev_fees'])}
            (+) Holobuildings: {self.format_currency(data['rev_holobuilding'])}
            (+) Interest: {self.format_currency(data['rev_interest'])}
            (+) Other: {self.format_currency(data['rev_other'])}
            (-) Fraud: {self.format_currency(data['exp_fraud'])}
            (-) Bugs: {self.format_currency(data['exp_bugs'])}
            (-) Taxes: {self.format_currency(data['exp_taxes'])}
            (-) Salaries: {self.format_currency(data['exp_salaries'])}
            (-) Operational: {self.format_currency(data['exp_operational'])}
            (-) Acquisitions: {self.format_currency(data['exp_acquisitions'])}
            (-) Tile Upgrades (Reducer): {self.format_currency(data['exp_tile_upgrades'])}
            (-) Lit: {self.format_currency(data['exp_lit'])}
            (-) Ref Codes: {self.format_currency(data['exp_ref'])}
            (-) Other: {self.format_currency(data['exp_other'])}
            =====================================
            Health: {self.format_currency(data['health'])}
        """
      
    def format_currency(self,value):
        """Format a number as currency."""
        if value >= 0:
            return f"${value:,.2f}"
        else:
            return f"-${-value:,.2f}"

    def on_mount(self) -> None:
        """Focus the tabs when the app starts."""
        self.query_one(Tabs).focus()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Tabs(*self.tabs)
        yield Static(self.init_msg, id="static-report-header")
        yield Label(id="label-projection")
        yield Footer()

    def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
        """Handle TabActivated message sent by Tabs."""

        print(event.tab)
        label = self.query_one(Label)
        label.update(self.projections[event.tab.id]["text"])
        '''
        label = self.query_one(Label)
        if event.tab is None:
            # When the tabs are cleared, event.tab will be None
            label.visible = False
        else:
            label.visible = True
            label.update(event.tab.label)
        '''