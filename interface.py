import readline
import args
from dumper import Dumper

class Interface:
    def __init__(self):
        self.cli_args = args.parse()
        try:
            self.d = Dumper(self.cli_args.api_id,self.cli_args.api_hash)
        except KeyboardInterrupt as _:
            print("quit...")

        self.commands = {}
        self.channels = []

    def _run(self):
        head,*tail = input(">>").split()
        if head not in self.commands.keys():
            print("dtc: error: no command '{}'!".format(head))
        
    def run(self):
        while True:
            try:
                self._run()
            except KeyboardInterrupt as _:
                print("quit...")
                return
