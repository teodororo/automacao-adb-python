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

#     GRAVAR A TELA (VARIACAO DO PRINT)

def record_screen():
    print("GRAVANDO TELA")
    output = subprocess.Popen("adb shell screenrecord --time-limit 10 /sdcard/DCIM/example.mp4", shell=True, stdout=subprocess.PIPE)

def get_screen(serial):
    output = subprocess.Popen('adb -s %s shell uiautomator dump'%serial,shell=True,stdout=subprocess.PIPE).communicate()[0]
    print(output)
    output = subprocess.Popen('adb -s %s pull /sdcard/window_dump.xml'%serial,shell=True,stdout=subprocess.PIPE).communicate()[0]
    print(output)

'''
    TIRA PRINT DA TELA
def print_screen():
    print("Tirando print da tela")
    output = subprocess.Popen("adb shell screencap -p /sdcard/DCIM/screenshot.png", shell=True, stdout=subprocess.PIPE)
'''

def tap_screen(app_name, x, y):
    print("Abrindo %s" % app_name)
    output = subprocess.Popen("adb shell input tap %s %s" % (x, y), shell=True, stdout=subprocess.PIPE)
    time.sleep(5)
    #print_screen() -- funcao que tira print da tela
    print("Voltando a tela anterior")
    output = subprocess.Popen("adb shell input keyevent 4", shell=True, stdout=subprocess.PIPE)

def test_app(node, app_name):
    if node.attrib.get('text') == app_name:
        position = node.attrib.get('bounds').split(']')[0]
        position = position.replace("[", "").split(",")
        print("Testando APP")
        tap_screen(app_name, position[0], position[1])
    else:
        for n in node.findall('node'):
            test_app(n, app_name)

def get_apps():
    xml = ET.parse('window_dump.xml')
    root = xml.getroot()
    app = test_app(root, 'Wikipédia')


device = get_devices()
record_screen()
get_screen(device)
get_apps()



