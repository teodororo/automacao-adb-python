import subprocess
import xml.etree.ElementTree as ET
import time


def get_devices():
    output = subprocess.Popen('adb devices', shell=True, stdout=subprocess.PIPE).communicate()[0]
    output = str(output).split('attached')[1]
    output = output.split('device')[0]
    output = output.replace("\\n", "").replace("\\r", "")
    output = output.replace("\\t", "")
    return output

'''     GRAVAR A TELA     '''
def record_screen():
    print("GRAVANDO TELA")
    output = subprocess.Popen("adb shell screenrecord --time-limit 20 /sdcard/DCIM/example.mp4", shell=True, stdout=subprocess.PIPE)

def event_home():
    print("Voltando a tela inicial")
    output = subprocess.Popen("adb shell input keyevent 3", shell=True, stdout=subprocess.PIPE)
    time.sleep(2)

def event_back():
    print("Voltando a tela anterior")
    output = subprocess.Popen("adb shell input keyevent 4", shell=True, stdout=subprocess.PIPE)
    time.sleep(2)

def swipe_screen():
    output = subprocess.Popen("adb shell input swipe 300 2000 300 500 500", shell=True, stdout=subprocess.PIPE)
    time.sleep(2)

def get_screen(serial):
    output = subprocess.Popen('adb -s %s shell uiautomator dump'%serial,shell=True,stdout=subprocess.PIPE).communicate()[0]
    print(output)
    output = subprocess.Popen('adb -s %s pull /sdcard/window_dump.xml'%serial,shell=True,stdout=subprocess.PIPE).communicate()[0]
    print(output)

def tap_screen(app_name, x, y):
    print("Abrindo %s" % app_name)
    output = subprocess.Popen("adb shell input tap %s %s" % (x, y), shell=True, stdout=subprocess.PIPE)

def test_app(node, app_name):
    if node.attrib.get('text') == app_name:
        position = node.attrib.get('bounds').split(']')[0]
        position = position.replace("[", "").split(",")
        print("Testando APP")
        tap_screen(app_name, position[0], position[1])
    else:
        for n in node.findall('node'):
            test_app(n, app_name)

def get_apps(name_app):
    xml = ET.parse('window_dump.xml')
    root = xml.getroot()
    app = test_app(root, name_app)

def search(search_text):
    get_screen(device)
    time.sleep(2)
    get_apps('Pesquisar ou digitar endereço da Web')
    time.sleep(2)
    output = subprocess.Popen("adb shell input text %s" %search_text, shell=True, stdout=subprocess.PIPE)
    time.sleep(1)
    output = subprocess.Popen("adb shell input keyevent 66", shell=True, stdout=subprocess.PIPE)
    time.sleep(2)
    swipe_screen()
    event_back()
    event_home()


device = get_devices()
record_screen()
get_screen(device)
get_apps('Chrome')
search('hefesto%suea')

'''
def open_app():
    output = subprocess.Popen("adb shell monkey -p com.android.chrome 1", shell=True, stdout=subprocess.PIPE)
    text()
'''
