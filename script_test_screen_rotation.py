import subprocess
import xml.etree.ElementTree as ET
import time

def record_screen():
    print("RECORDING THE SCREEN")
    subprocess.Popen("adb shell screenrecord --time-limit 7 /sdcard/DCIM/screen_rotation.mp4", shell=True, stdout=subprocess.PIPE)
    time.sleep(3)

def get_devices():
    output = subprocess.Popen('adb devices', shell=True, stdout=subprocess.PIPE).communicate()[0]
    output = str(output).split('attached')[1]
    output = output.split('device')[0]
    output = output.replace("\\n", "").replace("\\r", "")
    output = output.replace("\\t", "")
    return output

def get_screen(serial):
    print("CREATING WINDOW_DUMP.XML")
    subprocess.Popen('adb -s %s shell uiautomator dump'%serial,shell=True,stdout=subprocess.PIPE).communicate()[0]
    subprocess.Popen('adb -s %s pull /sdcard/window_dump.xml'%serial,shell=True,stdout=subprocess.PIPE).communicate()[0]

def tap_screen(app_name, x, y):
    print("OPENING %s" % app_name)
    subprocess.Popen("adb shell input tap %s %s" % (x, y), shell=True, stdout=subprocess.PIPE)
    time.sleep(3)

def test_app(node, app_name):
    if node.attrib.get('text') == app_name:
        position = node.attrib.get('bounds').split(']')[0]
        position = position.replace("[", "").split(",")
        print("TESTING APP")
        tap_screen(app_name, position[0], position[1])
    else:
        for n in node.findall('node'):
            test_app(n, app_name)

def get_apps(name_app):
    xml = ET.parse('window_dump.xml')
    root = xml.getroot()
    app = test_app(root, name_app)

def screen_rotation(serial):
    print("TURNING OFF AUTOMATIC SCREEN ROTATION")
    subprocess.Popen('adb -s %s shell content insert --uri content://settings/system --bind name:s:accelerometer_rotation --bind value:i:0'%serial,shell=True,stdout=subprocess.PIPE).communicate()[0]
    print("LANDSCAPE MODE")
    subprocess.Popen('adb -s %s shell content insert --uri content://settings/system --bind name:s:user_rotation --bind value:i:1'%serial,shell=True,stdout=subprocess.PIPE).communicate()[0]
    time.sleep(3)
    print("PORTRAIT MODE")
    subprocess.Popen('adb -s %s shell content insert --uri content://settings/system --bind name:s:user_rotation --bind value:i:0'%serial,shell=True,stdout=subprocess.PIPE).communicate()[0]
    time.sleep(3)
    print("CHANGING TO HOME")
    subprocess.Popen("adb shell input keyevent 3", shell=True, stdout=subprocess.PIPE)
    time.sleep(3)


def get_record(serial):
    time.sleep(5)
    print("PULLING .mp4")
    subprocess.Popen('adb -s %s pull /sdcard/DCIM/screen_rotation.mp4'%serial, shell=True, stdout=subprocess.PIPE)

record_screen()
device = get_devices()
get_screen(device)
get_apps('Telefone')
screen_rotation(device)
get_record(device)

