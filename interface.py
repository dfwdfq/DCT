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


    def run(self):
        pass
