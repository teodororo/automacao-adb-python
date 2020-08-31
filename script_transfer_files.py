import subprocess
import xml.etree.ElementTree as ET
import time


# Create file
def create_dir():
    # Command below might not work if you don't have root permissions 
    process = subprocess.Popen('adb shell mkdir test_directory', shell=True, stdout=subprocess.PIPE)
    process = subprocess.Popen('adb shell cd ./test_directory', shell=True, stdout=subprocess.PIPE)
    process = subprocess.Popen('adb shell touch example.png', shell=True, stdout=subprocess.PIPE)

def create_copy():
    # a ->  preserve the specified attributes
    # v -> verbose output
    # r -> Copy directories recursively
    process = subprocess.Popen('adb shell cp -avr test_directory ./sdcard', shell=True, stdout=subprocess.PIPE)

def rename_dir():
    # Using mv command
    process = subprocess.Popen('adb shell mv test_directory new_directory', shell=True, stdout=subprocess.PIPE)
    
def move_dir():
    process = subprocess.Popen('adb shell mv new_directory ./sdcard', shell=True, stdout=subprocess.PIPE)

def remove_dir():
    # Removes the old and the copy
    process = subprocess.Popen('adb shell cd ./sdcard', shell=True, stdout=subprocess.PIPE)
    process = subprocess.Popen('adb shell rm -r test_directory', shell=True, stdout=subprocess.PIPE)
    process = subprocess.Popen('adb shell rm -r new_directory', shell=True, stdout=subprocess.PIPE)
    

create_dir()
create_copy()
rename_dir()
move_dir()
remove_dir()
