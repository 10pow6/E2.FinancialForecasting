from textual.message import Message

class ScreenFlowEvent( Message ):
        def __init__( self, id: str, desc:str=None, data:dict=None ) -> None:
            super().__init__()
            self.id = id
            self.desc=desc
            self.data=data