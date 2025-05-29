import argparse

def parse():
    parser = argparse.ArgumentParser(description="CLI to dump telegram channel data.")
    parser.add_argument('api_id', type=str, help='telegram API id.')
    parser.add_argument("api_hash",type=str,help="telegram API hash.")
    parser.add_argument("--media", "--m",help="media directory", default="media")
    parser.add_argument("--output","--o",help="output file",default="output.jsonl")
    parser.add_argument("--session","--s",help="session file",default="")
    
    return parser.parse_args()
