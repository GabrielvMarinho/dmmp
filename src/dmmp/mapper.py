import os
from tqdm import tqdm

class Mapper():
   def __init__(self, save_path: str, folders_to_ignore: list[str], metadata_file_name: str="desc"):
      self.folders_to_ignore = {item for item in folders_to_ignore}
      self.save_path = save_path
      self.progress_bar = tqdm(total=100)
      self.folders_sum = 0
      self.metadata_file_name = metadata_file_name
      self.temp_mapping = {}
   
   def __call__(self, dir_to_map: str):
      for index, array in enumerate(dir_to_map):
         path = array[0]
         nested_folders = int(array[1])
         load_bar_start = index/len(dir_to_map)*100
         load_bar_end = (index+1)/len(dir_to_map)*100
         self.read_dir(path, nested_folders, load_bar=True, load_bar_start=load_bar_start, load_bar_end=load_bar_end)
      self.write_map()
      self.update_progress_bar(percentage=100, post_fix="Finished", close=True)
      print(f"{self.folders_sum} folders were scanned.")

   def update_progress_bar(self, percentage: float, post_fix: str, close: bool=False):
      self.progress_bar.n = float(f"{percentage:.2f}")
      self.progress_bar.refresh()
      self.progress_bar.set_postfix_str(post_fix)
      if close:
         self.progress_bar.close()

   def read_dir(self, directory: str, max_rec: int, current_rec: int=0, load_bar: bool=False, load_bar_start: int=0, load_bar_end: int=100):
      if directory.endswith(f"{self.metadata_file_name}.dmmp"):
         self.get_desc_data(directory)
      if current_rec>max_rec or not os.path.isdir(directory):
         return
      folders = os.listdir(directory)
      
      for index, folder in enumerate(folders):
         if folder not in self.folders_to_ignore:      
            self.read_dir(fr"{directory}\{folder}", max_rec=max_rec, current_rec=current_rec+1)
            self.folders_sum = self.folders_sum+1
         if load_bar:
            percentage = index/len(folders)
            diff = load_bar_end-load_bar_start
            relative_percentage = (percentage*diff)+load_bar_start
            self.update_progress_bar(percentage=relative_percentage, post_fix=folder)

   def get_desc_data(self, directory: str):
      with open(directory, "r", encoding="utf-8") as f:
            id = f.readline().strip()
            name = f.readline().strip()
            desc = f.readline().strip()
            type_ = f.readline().strip()
            relationships = f.readline().split(",")
            self.temp_mapping[id] = {            
               "name":name,
               "desc":desc,
               "folder":type_,
               "type":type_,
               "relationships":relationships,
               "origin":"/".join(directory.split("\\")[:-1])
            }

   def write_map(self):
      for _, object in self.temp_mapping.items():
         path = self.save_path+"/"+object.get("folder")
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
         self.temp_mapping.get(rel.strip()) for rel in object.get("relationships")
         ]
   ])
      }
      """)