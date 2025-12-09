from dotenv import load_dotenv
import argparse
from mapper import Mapper

load_dotenv()

parser = argparse.ArgumentParser(
   prog="DMM",
   description="Directory Metadata Mapper"
)
parser.add_argument('-d', '--dir-to-map', required=True, help="Directory to scan + number of nested folders to iterate", nargs=2, action="append")
parser.add_argument('-i', '--folders-ignore', required=False, help="List of folders to ignore", nargs="+")
parser.add_argument('-s', '--save-path', required=True, help="Path to save output")
parser.add_argument('-m', '--metadata-file-name', required=True, help="File name containing the directory metadata (no extension)")

args = parser.parse_args()

if __name__ == "__main__":
   mapper = Mapper(args.save_path, args.folders_ignore, args.metadata_file_name)
   mapper(args.dir_to_map)
   