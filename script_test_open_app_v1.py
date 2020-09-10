'''
    Algoritmo script_test_open_app_v1.py
    Autores: Diego Torres, Giovanna S. Teodoro e João Guilherme S. Gomes
    Descrição: O algoritmo automatiza uma série de comandos adb (android debug bridge) que realizam em um device (os testes foram
               realizados em um emulador android pixel 3 com Android 9) a operação de abertura de um determinado app (no caso a
               Play Store).
    OBS: a numeração no início de cada descrição de função representa a ordem de execução das funções. A descrição completa do
         código encontra-se em bit.ly/hefesto7-doc
'''
import subprocess
import xml.etree.ElementTree as ET
import time

'''  (1) - Function get_devices()  '''

def get_devices():
    output = subprocess.Popen('adb devices', shell=True, stdout=subprocess.PIPE).communicate()[0]
    output = str(output).split('attached')[1]
    output = output.split('device')[0]
    output = output.replace("\\n", "").replace("\\r", "")
    output = output.replace("\\t", "")
    return output

'''  (2) - Function get_screen()  '''

def get_screen(serial):
    output = subprocess.Popen('adb -s %s shell uiautomator dump'%serial,shell=True,stdout=subprocess.PIPE).communicate()[0]
    print(output)
    output = subprocess.Popen('adb -s %s pull /sdcard/window_dump.xml'%serial,shell=True,stdout=subprocess.PIPE).communicate()[0]
    print(output)

''' (5) - Function tap_screen()  '''

def tap_screen(app_name, x, y):
    print("Abrindo %s" % app_name)
    output = subprocess.Popen("adb shell input tap %s %s" % (x, y), shell=True, stdout=subprocess.PIPE)
    time.sleep(5)
    print("Voltando a tela anterior")
    output = subprocess.Popen("adb shell input keyevent 4", shell=True, stdout=subprocess.PIPE)

''' (4) - Function test_app()  '''

def test_app(node, app_name):
    if node.attrib.get('text') == app_name:
        position = node.attrib.get('bounds').split(']')[0]
        position = position.replace("[", "").split(",")
        print("Testando APP")
        tap_screen(app_name, position[0], position[1])
    else:
        for n in node.findall('node'):
            test_app(n, app_name)

'''  (3) - Function get_apps()  '''

def get_apps():
    xml = ET.parse('window_dump.xml')
    root = xml.getroot()
    app = test_app(root, 'Play Store')


device = get_devices()
get_screen(device)
get_apps()
