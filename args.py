import argparse

def parse():
    parser = argparse.ArgumentParser(description="CLI to dump telegram channel data.")
    parser.add_argument('api_id', type=str, help='telegram API id.')
    parser.add_argument("api_hash",type=str,help="telegram API hash.")
    return parser.parse_args()
