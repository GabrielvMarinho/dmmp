from dotenv import load_dotenv
import argparse
import os
from .mapper import Mapper
from .args import get_args, validate_args, write_args_to_toml


if __name__ == "__main__":

   load_dotenv()  

   parser = argparse.ArgumentParser(
      prog="DMM",
      description="Directory Metadata Mapper"
   )
   parser.add_argument('-c', '--config-file', default="config.toml", required=False, help=".toml file to get configuration from ") 
   parser.add_argument('-d', '--dir-to-map', required=False, help="Directory to scan + number of nested folders to iterate", nargs=2, action="append")
   parser.add_argument('-i', '--folders-ignore', required=False, help="List of folders to ignore", nargs="+")
   parser.add_argument('-s', '--save-path', required=False, help="Path to save output")
   parser.add_argument('-n', '--name-output', required=False, help="Name of the output directory")
   parser.add_argument('-m', '--metadata-file-names', required=False, nargs="+", help="File names containing the directory metadata (no extension)")

   required_args = [
      "dir_to_map",
      "folders_ignore",
      "save_path",
      "name_output",
      "metadata_file_names",
      ]

   args = parser.parse_args()

   formatted_args = get_args(args)
   
   validate_args(formatted_args, required_args=required_args)

   mapper = Mapper(formatted_args.get("save_path"),
                  formatted_args.get("name_output"), 
                  formatted_args.get("folders_ignore"), 
                  formatted_args.get("metadata_file_names"))
   mapper(formatted_args.get("dir_to_map"))
   
   write_args_to_toml(formatted_args, formatted_args["config_file"])