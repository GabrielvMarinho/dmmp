import sys
from pathlib import Path
import pytest

new_lib_path = str(Path(__file__).resolve().parents[1])

sys.path.append(new_lib_path)

from src.dmmp.mapper import Mapper
import os

mapper = Mapper("", "", ["desc"], ["*"])


def test_get_link():
   mapper._temp_mapping = {
      "id":{
         "folder":"/path/here",
         "name":"test"
      }
   }
   assert(mapper._get_link("id") == "/path/here/test|test")
   mapper._temp_mapping = {}

def test_get_desc_data():
   
   mapper._get_desc_data(os.path.join(
         "tests", 
         "test_content", 
         "desc.dmmp"))
   
   assert(
      mapper._temp_mapping == 
         {
            "123":{
               "name":"data",
               "desc":"data",
               "folder":"data/",
               "origin":"tests/test_content/desc.dmmp"
            }
         }
      )

def test_update_progress_bar():
   mapper._update_progress_bar(50, "Task 5")   
   assert(mapper._progress_bar.postfix == "Task 5")
   assert(mapper._progress_bar_percentage == 50)

def test_write_map():
   pass
