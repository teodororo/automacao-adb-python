import subprocess
import xml.etree.ElementTree as ET
import time

 
# Creates file
def create_dir():
    # Command below might not work if you don't have root permissions 
    print("CREATING DIRECTORY")
    subprocess.Popen('adb shell mkdir test_directory', shell=True, stdout=subprocess.PIPE)
    time.sleep(5)
    print("CREATING FILE INSIDE ./test_directory")
    subprocess.Popen('adb shell touch /test_directory/example.txt', shell=True, stdout=subprocess.PIPE)
    time.sleep(5)


# Creates a copy of example.txt 
def create_copy():
    print("CREATING COPY") 
    subprocess.Popen('adb shell cp /test_directory/example.txt /', shell=True, stdout=subprocess.PIPE)
    time.sleep(5)

# Changes directory's name 
def rename_dir():
    print("CHANGING DIRECTORY'S NAME") 
    # Using mv command
    subprocess.Popen('adb shell mv test_directory new_directory', shell=True, stdout=subprocess.PIPE)
    time.sleep(5) 

# Changes directory's path  
def move_dir():
    print("MOVING DIRECTORY") 
    subprocess.Popen('adb shell mv new_directory /sdcard', shell=True, stdout=subprocess.PIPE)
    time.sleep(5) 

def remove_dir_and_file():
    # Removes the old and the copy
    print("REMOVING DIRECTORY AND FILE") 
    subprocess.Popen('adb shell rm example.txt', shell=True, stdout=subprocess.PIPE)
    subprocess.Popen('adb shell rm -r /sdcard/new_directory', shell=True, stdout=subprocess.PIPE)


create_dir()
create_copy()
rename_dir()
move_dir()
remove_dir_and_file()
