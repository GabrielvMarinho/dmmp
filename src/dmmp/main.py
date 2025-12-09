import os
from dotenv import load_dotenv
import argparse

parser = argparse.ArgumentParser(
   prog="dmm",
   description="directory metadata mapper"
)
parser.add_argument('-d', '--dir-to-map', required=True, help="directory to scan + number of nested folders to iterate", nargs=2, action="append")
parser.add_argument('-i', '--folders-ignore', required=False, help="list of folders to ignore", nargs="+")


load_dotenv()
args = parser.parse_args()


map = os.getenv("PATH_TO_SAVE_MAP")

folders_to_ignore = {item for item in os.getenv("FOLDERS_TO_IGNORE").split(",")}
sum_ = {}

structure = {}

def read_dir(dir_, max_rec, current_rec=0, load_bar=False, load_bar_start=0, load_bar_end=100):

   if dir_.endswith("desc.dmmp"):
      with open(dir_, "r", encoding="utf-8") as f:
         id = f.readline().strip()
         name = f.readline().strip()
         desc = f.readline().strip()
         type_ = f.readline().strip()
         relationships = f.readline().split(",")
         structure[id] = {            
            "name":name,
            "desc":desc,
            "folder":type_,
            "type":type_,
            "relationships":relationships,
            "origin":"/".join(dir_.split("\\")[:-1])
         }
   
   if not os.path.isdir(dir_):
      return
   
   if current_rec>max_rec:
      return
   
   global sum
   folders = os.listdir(dir_)
   if load_bar:
      for index, folder in enumerate(folders):
         percentage = index/len(folders)
         diff = load_bar_end-load_bar_start
         relative_percentage = (percentage*diff)+load_bar_start
         print(f"----- {relative_percentage:.2f}% -> {folder}")
         if folder not in folders_to_ignore:      
            read_dir(fr"{dir_}\{folder}", max_rec=max_rec, current_rec=current_rec+1)
            sum_[folder] = (sum_.get(folder) or 0) + 1
   else:
      for folder in folders:
         if folder not in folders_to_ignore:      
            read_dir(fr"{dir_}\{folder}", max_rec=max_rec, current_rec=current_rec+1)
            sum_[folder] = (sum_.get(folder) or 0) + 1

def write_map():
   for id, object in structure.items():
      path = map+"/"+object.get("folder")
      os.makedirs(path, exist_ok=True)
      with open(f"{path}/{object.get("name")}.md", "w", encoding="utf-8") as f1:
         f1.write(f"""
{object.get("desc")}

type: {object.get("type")}
location: {object.get("origin")}

relationships: {
   ", ".join([
      f"[[{rel.get("name")}]]" if rel else "" 
      for rel in [
         structure.get(rel.strip()) for rel in object.get("relationships")
         ]
   ])
   }
   """)
   
 
          
if __name__ == "__main__":
   
   print(args.dir_to_map)
   print(args.folders_ignore)

   for index, array in enumerate(args.dir_to_map):
      path = array[0]
      nested_folders = int(array[1])
      load_bar_start = index/len(args.dir_to_map)*100
      load_bar_end = (index+1)/len(args.dir_to_map)*100
      read_dir(path, nested_folders, load_bar=True, load_bar_start=load_bar_start, load_bar_end=load_bar_end)
   print("----- 100% -----")
   print(structure)
   write_map()