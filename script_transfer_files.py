import subprocess
import xml.etree.ElementTree as ET
import time


# Create file
def create_dir():
    # Command below might not work if you don't have root permissions 
    subprocess.Popen('adb shell mkdir diretorio_teste', shell=True, stdout=subprocess.PIPE)
    subprocess.Popen('adb shell cd ./diretorio_teste', shell=True, stdout=subprocess.PIPE)
    subprocess.Popen('adb shell touch example.png', shell=True, stdout=subprocess.PIPE)

'''
def create_copy():

def rename_dir():

def move_dir():

def remove_dir():
    subprocess.Popen('adb shell rm -r test_directory', shell=True, stdout=subprocess.PIPE)

'''
create_dir()
'''
create_copy()
rename_dir()
move_dir()
remove_dir()
'''
