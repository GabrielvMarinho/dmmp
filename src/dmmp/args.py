import tomllib
import tomli_w
import os
from .exceptions import MissingArgumentException


def _get_toml_args(path: str):
   try:
      with open(path, "rb") as f:
         data = tomllib.load(f)
         return data
      
   except Exception as e:
      print(e)
      return {}


def get_args(args):
   toml_dict = _get_toml_args(args.config_file)

   cli_dict = {
      k:v for k, v in {
      "config_file":args.config_file,
      "dir_to_map":args.dir_to_map,
      "folders_ignore":args.folders_ignore,
      "save_path":args.save_path,
      "name_output":args.name_output,
      "metadata_file_names":args.metadata_file_names,
      }.items() if v !=None
   }
   merged_dict = toml_dict | cli_dict

   # the reason for this is, cli arguments should be priority, but only if its not a default one, 
   # default ones will ONLY be written if the toml ones are empty
   merged_dict["folders_ignore"] = [] if not merged_dict.get("folders_ignore") else merged_dict["folders_ignore"] 
   merged_dict["save_path"] = os.getcwd() if not merged_dict.get("save_path") else merged_dict["save_path"] 
   merged_dict["name_output"] = "dmmp-output" if not merged_dict.get("name_output") else merged_dict["name_output"] 
   merged_dict["config_file"] = "config.toml" if not merged_dict.get("config_file") else merged_dict["config_file"] 
   merged_dict["metadata_file_names"] = ["*"] if not merged_dict.get("metadata_file_names") else merged_dict["metadata_file_names"] 

   return merged_dict


def validate_args(args: dict, required_args: list[str]):
   for arg in required_args:
      if arg not in args.keys():
         raise MissingArgumentException(arg)
    

def write_args_to_toml(args: dict, config_file_name: str):
   with open(os.path.join(os.getcwd(), config_file_name), "wb") as f:
      tomli_w.dump(args, f)
 