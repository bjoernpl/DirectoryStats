# DirectoryStats

A python CLI for efficient analysis of folder size and contents, especially for large amounts of files.

## Usage
`python -m main.py [dir_name]`

This command counts the total amount of files in a given directory and all subfolders. It also gives additional
information such as amount of subfolders and total directory size. 

Subsequent evaluations of folders are much faster than the first run, while the first run is already significantly faster
than the `right-click folder -> properties` inspection on linux and windows.

## TODO
- clean up code
- rename files to better convey their function
- remove unnecessary files
- implement caching correctly
- add more command line flags
  - which stats to output
  - where to place cache
  - shallow inspection (?)
- make PyPi module
