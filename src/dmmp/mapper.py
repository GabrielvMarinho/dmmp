import os
from tqdm import tqdm

class Mapper():
   def __init__(self, save_path, folders_to_ignore):
      self.folders_to_ignore = {item for item in folders_to_ignore}
      self.save_path = save_path
      self.progress_bar = tqdm(total=100)
      self.sum_folder = 0
      self.temp_mapping = {}
   
   def __call__(self, dir_to_map):
      for index, array in enumerate(dir_to_map):
         path = array[0]
         nested_folders = int(array[1])
         load_bar_start = index/len(dir_to_map)*100
         load_bar_end = (index+1)/len(dir_to_map)*100
         self.read_dir(path, nested_folders, load_bar=True, load_bar_start=load_bar_start, load_bar_end=load_bar_end)
      self.write_map()

   def read_dir(self, dir_, max_rec, current_rec=0, load_bar=False, load_bar_start=0, load_bar_end=100):
      if dir_.endswith("desc.dmmp"):
         with open(dir_, "r", encoding="utf-8") as f:
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
            self.progress_bar.n = float(f"{relative_percentage:.2f}")
            self.progress_bar.refresh()
            self.progress_bar.set_postfix(task=folder)
            if folder not in self.folders_to_ignore:      
               self.read_dir(fr"{dir_}\{folder}", max_rec=max_rec, current_rec=current_rec+1)
               self.sum_folder = self.sum_folder+1
      else:
         for folder in folders:
            if folder not in self.folders_to_ignore:      
               self.read_dir(fr"{dir_}\{folder}", max_rec=max_rec, current_rec=current_rec+1)
               self.sum_folder = self.sum_folder+1

   def write_map(self):
      for id, object in self.temp_mapping.items():
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