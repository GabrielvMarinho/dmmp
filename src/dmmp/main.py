from dotenv import load_dotenv
import argparse
from mapper import Mapper

load_dotenv()

parser = argparse.ArgumentParser(
   prog="dmm",
   description="directory metadata mapper"
)
parser.add_argument('-d', '--dir-to-map', required=True, help="directory to scan + number of nested folders to iterate", nargs=2, action="append")
parser.add_argument('-i', '--folders-ignore', required=False, help="list of folders to ignore", nargs="+")
parser.add_argument('-s', '--save-path', required=True, help="path to save output")

args = parser.parse_args()

if __name__ == "__main__":
   mapper = Mapper(args.save_path, args.folders_ignore)
   mapper(args.dir_to_map)
   