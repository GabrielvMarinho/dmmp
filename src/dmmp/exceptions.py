class NotEmptyDir(Exception):
   def __init__(self, path):
      super().__init__(f"Output directory ({path}) not empty, cannot overwrite it")