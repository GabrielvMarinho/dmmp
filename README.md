# DMMP - Directory Metadata Mapper Protocol
Mapper that generates a group of .md files that represent a specific directory in a file system path, creating linked files that follow the [markdown syntax](https://www.markdownguide.org/).

## Standard metadata format
```ddmp
unique_id
output_folder_path/
output_file_name
output_file_description
```

Populate a specific directory and its subdirectories in this fashion before building the output (in .dmmp files).

After doing so, run something like the following:
```
python -m dmmp -d "C:\Path1" 1 -s "C:\Path2" -m "name"
```
C:\Path1 -> path of input.  
1 -> number of nested folders to check.  
C:\Path2 -> path of output.  
name -> name on which the metadata files will be on, without extension.

Now on the output path, you should see a tree of folders that represent the data you provided as input.