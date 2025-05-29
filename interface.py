import readline
import args
import pydoc
import pandas as pd
from dumper import Dumper
from tabulate import tabulate

class Interface:
    def __init__(self):
        self.cli_args = args.parse()
        try:
            self.d = Dumper(self.cli_args.api_id,self.cli_args.api_hash)
        except KeyboardInterrupt as _:
            print("quit...")

        self.commands = {
            "list":self._list_channels,
            "dump":self._dump
        }
        self.channels = []

    def _list_channels(self,args:list, should_print: bool = True) -> None:
        """list available channels."""
        self.channels = self.d.list_available_channels()
        data = {
            "name":[],
            "telegram id":[]
        }
        counter = 0
        for ch in self.channels:
            data["name"].append(ch["title"])
            data["telegram id"].append(ch["id"])
            counter += 1
        
        self.df = pd.DataFrame(data)
        table = tabulate(self.df, headers='keys', tablefmt='psql')
        if should_print: pydoc.pager(table)

    def _get_channel_id(self, inner_id:int):
        pass
    def _dump(self, args:list) -> None:
        """dump channel using its id."""
        if len(args) != 1:
            print("dtc: error: dump requires exactly 1 argument that is channel id!")
            return

        inner_id = args[0]
        if not inner_id.isdigit():
            print("dtc: error: '{}' should be integer!".format(inner_id))
            return
        inner_id = int(inner_id)

        try:
            if not hasattr(self,"df"):self._list_channels([],False)#create df
                
            row = self.df.iloc[inner_id]
            ch_id = row["telegram id"]
            self.d.dump_channel_by_id(ch_id)
            
        except IndexError as _:
            print("dtc: error: '{} doesn't exist!".format(inner_id))
            return
        
        
    def _run(self) -> None:
        head,*tail = input(">>").split()
        if head not in self.commands.keys():
            print("dtc: error: no command '{}'!".format(head))
        else:
            self.commands[head](tail)
        
    def run(self) -> None:
        while True:
            try:
                self._run()
            except KeyboardInterrupt as _:
                print("quit...")
                return
