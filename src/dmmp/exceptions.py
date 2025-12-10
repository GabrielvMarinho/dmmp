class DirectoryAlreadyExists(Exception):
   def __init__(self, path):
      super().__init__(f"Output directory ({path}) already exists, cannot overwrite it")