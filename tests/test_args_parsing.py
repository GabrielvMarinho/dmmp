import sys
from pathlib import Path
import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.dmmp.args import _get_toml_args, validate_args, write_args_to_toml
from src.dmmp.exceptions import MissingArgumentException
import os

generic_dict = {"data1":"1", "data2":"2"}

def test_get_toml_args():
   data = _get_toml_args(os.path.join(os.getcwd(), "tests", "config.toml"))
   assert data == {"data":"test"}

def test_validate_args():
   validate_args(generic_dict, ["data1", "data2"])

   with pytest.raises(MissingArgumentException):
      validate_args({"not_data1":"1", "data2":"2"}, ["data1", "data2"])

def test_write_args_to_toml():
   path = os.path.join(os.getcwd(), "tests", "temp.toml")
   write_args_to_toml(generic_dict, path)
   data = _get_toml_args(path)
   assert data == generic_dict  
   os.remove(path)