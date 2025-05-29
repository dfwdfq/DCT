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

        self.commands = {"list":self._list_channels}
        self.channels = []

    def _list_channels(self,args:list) -> None:
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
            
        df = pd.DataFrame(data)
        table = tabulate(df, headers='keys', tablefmt='psql')
        pydoc.pager(table)
        
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
