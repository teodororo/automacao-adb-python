import subprocess
import xml.etree.ElementTree as ET
import time


def record_screen():
    print("GRAVANDO TELA")
    subprocess.Popen("adb shell screenrecord --time-limit 20 /sdcard/DCIM/install_and_test.mp4", shell=True, stdout=subprocess.PIPE)
    time.sleep(3)

def get_devices():
    output = subprocess.Popen('adb devices', shell=True, stdout=subprocess.PIPE).communicate()[0]
    output = str(output).split('attached')[1]
    output = output.split('device')[0]
    output = output.replace("\\n", "").replace("\\r", "")
    output = output.replace("\\t", "")
    return output
  
def get_screen(serial):
    print("CRIANDO WINDOW_DUMP.XML")
    output = subprocess.Popen('adb -s %s shell uiautomator dump'%serial,shell=True,stdout=subprocess.PIPE).communicate()[0]
    print(output)
    output = subprocess.Popen('adb -s %s pull /sdcard/window_dump.xml'%serial,shell=True,stdout=subprocess.PIPE).communicate()[0]
    print(output)


def tap_screen(app_name, x, y):
    print("ABRINDO %s" % app_name)
    output = subprocess.Popen("adb shell input tap %s %s" % (x, y), shell=True, stdout=subprocess.PIPE)
    time.sleep(5)
    print("VOLTANDO A TELA INICIAL")
    output = subprocess.Popen("adb shell input keyevent 3", shell=True, stdout=subprocess.PIPE)

def test_app(node, app_name):
    if node.attrib.get('text') == app_name:
        position = node.attrib.get('bounds').split(']')[0]
        position = position.replace("[", "").split(",")
        print("TESTANDO APP")
        tap_screen(app_name, position[0], position[1])
    else:
        for n in node.findall('node'):
            test_app(n, app_name)

def get_apps(name_app):
    xml = ET.parse('window_dump.xml')
    root = xml.getroot()
    app = test_app(root, name_app)

def install_apps():
    print("INSTALANDO APK")
    swipe_screen()
    output = subprocess.Popen("adb install ./apks/wikipedia.apk", shell=True, stdout=subprocess.PIPE)
   # output = subprocess.Popen("adb install ./apks/ankidroid.apk", shell=True, stdout=subprocess.PIPE)
    time.sleep(5)
   # output = subprocess.Popen("adb shell input keyevent 4", shell=True, stdout=subprocess.PIPE)

def swipe_screen():
    output = subprocess.Popen("adb shell input swipe 300 2000 300 500 200", shell=True, stdout=subprocess.PIPE)
    time.sleep(3)

def get_record():
    time.sleep(10)
    print("PASSANDO ARQUIVO GRAVADO PARA COMPUTADOR")
    output = subprocess.Popen("adb shell pull /sdcard/DCIM/example.mp4 .", shell=True, stdout=subprocess.PIPE)

device = get_devices() # passo 1 no original
record_screen()
install_apps()
# swipe_screen()
get_screen(device) # passo 2 no original
get_apps('Wikipédia') # passo 3 no original
get_record()

#get_apps('AnkiDroid')





# open_app() >>>>>>>>>>> CHAMADA DA FUNÇÃO
'''
-------------- ABRINDO APLICATIVO POR PACOTE --------------
def open_app():
    output = subprocess.Popen("adb shell monkey -p com.android.chrome 1", shell=True, stdout=subprocess.PIPE)
    text()
    
-------------- FUNÇÃO OPERATION (REALIZA PESQUISA NO CHROME) --------------
def operation():
    #get_screen(device)
    output = subprocess.Popen("adb shell input tap 77 630", shell=True, stdout=subprocess.PIPE)
    time.sleep(1)
    search = "hefesto%suea"
    output = subprocess.Popen("adb shell input text %s" %search, shell=True, stdout=subprocess.PIPE)
    time.sleep(1)
    output = subprocess.Popen("adb shell input keyevent 66", shell=True, stdout=subprocess.PIPE)
    time.sleep(2)
    output = subprocess.Popen("adb shell input swipe 300 2000 300 500", shell=True, stdout=subprocess.PIPE)
    time.sleep(1)
'''
