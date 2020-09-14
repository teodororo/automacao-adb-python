import subprocess
import xml.etree.ElementTree as ET
import time

def record_screen():
    print("GRAVANDO TELA")
    subprocess.Popen("adb shell screenrecord --time-limit 45 /sdcard/DCIM/date_and_hour", shell=True, stdout=subprocess.PIPE)
    time.sleep(2)

def get_devices():
    output = subprocess.Popen('adb devices', shell=True, stdout=subprocess.PIPE).communicate()[0]
    output = str(output).split('attached')[1]
    output = output.split('device')[0]
    output = output.replace("\\n", "").replace("\\r", "")
    output = output.replace("\\t", "")
    return output

def swipe_screen():
    output = subprocess.Popen("adb shell input swipe 300 2000 300 500 200", shell=True, stdout=subprocess.PIPE)
    time.sleep(2)

def get_apps(name_app):
    xml = ET.parse('window_dump.xml')
    root = xml.getroot()
    app = test_app(root, name_app)

def get_screen(serial):
    print("CRIANDO WINDOW_DUMP.XML")
    output = subprocess.Popen('adb -s %s shell uiautomator dump'%serial,shell=True,stdout=subprocess.PIPE).communicate()[0]
    print(output)
    output = subprocess.Popen('adb -s %s pull /sdcard/window_dump.xml'%serial,shell=True,stdout=subprocess.PIPE).communicate()[0]
    print(output)
    time.sleep(2)

def tap_screen(app_name, x, y):
    print("ABRINDO %s" % app_name)
    output = subprocess.Popen("adb shell input tap %s %s" % (x, y), shell=True, stdout=subprocess.PIPE)
    time.sleep(1)

def test_app(node, app_name):
    time.sleep(1)
    if node.attrib.get('text') == app_name:
        position = node.attrib.get('bounds').split(']')[0]
        position = position.replace("[", "").split(",")
        print("TESTANDO APP")
        tap_screen(app_name, position[0], position[1])
    else:
        for n in node.findall('node'):
            test_app(n, app_name)

def get_record(serial):
    time.sleep(3)
    print("PASSANDO ARQUIVO GRAVADO PARA COMPUTADOR")
    output = subprocess.Popen('adb -s %s pull /sdcard/DCIM/date_and_hour.mp4'%serial, shell=True, stdout=subprocess.PIPE)


record_screen()
device = get_devices()
swipe_screen()
get_screen(device)
get_apps('Configurações')
get_screen(device)
get_apps('Sistema')
get_screen(device)
get_apps('Data e hora')
get_screen(device)
get_apps('Definir data')
get_screen(device)
get_apps('14')
get_apps('OK')
get_screen(device)
get_apps('Definir hora')
get_screen(device)
get_apps('3')
get_screen(device)
get_apps('55')
get_apps('OK')
get_record(device)

