#o python só importa um unico arquivo como modulo. Esse script aqui é pra organizar todas as funcionalidades dos scripts
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

def print_screen(caminho_para_salvar = "/sdcard/DCIM/screenshot.png"):
    print("Tirando print da tela")
    subprocess.Popen("adb shell screencap -p " + caminho_para_salvar, shell=True, stdout=subprocess.PIPE)
    print("Salvo no dispositivo em", caminho_para_salvar)
    obter_arquivo(caminho_para_salvar)

def obter_arquivo(caminho):
    print("Obtendo arquivo, aguarde...")
    time.sleep(2)
    subprocess.Popen("adb pull "+caminho+" .",shell=True, stdout=subprocess.PIPE)
    print("Concluido")

def record_screen(limite_tempo = 10, caminho = "/sdcard/DCIM/example.mp4"):
    print("GRAVANDO TELA")
    print("adb shell screenrecord --time-limit " + str(limite_tempo)+" "+caminho)
    subprocess.Popen("adb shell screenrecord --time-limit " + str(limite_tempo)+" "+caminho, shell=True, stdout=subprocess.PIPE).wait()
    obter_arquivo(caminho)


def get_elements_screen(serial = get_devices()):#obtem um xml com as posições de cada app
    output = subprocess.Popen('adb -s %s shell uiautomator dump'%serial,shell=True,stdout=subprocess.PIPE).communicate()[0]
    print(output)
    output = subprocess.Popen('adb -s %s pull /sdcard/window_dump.xml'%serial,shell=True,stdout=subprocess.PIPE).communicate()[0]
    print(output)

def tap_screen(app_name, x, y):
    print("Abrindo %s" % app_name)
    output = subprocess.Popen("adb shell input tap %s %s" % (x, y), shell=True, stdout=subprocess.PIPE)
    time.sleep(5)
    #print_screen() -- funcao que tira print da tela
    print("Voltando a tela anterior")
    output = subprocess.Popen("adb shell input keyevent 4", shell=True, stdout=subprocess.PIPE)

def open_app(node, app_name):#Abre o app
    if node.attrib.get('text') == app_name:
        position = node.attrib.get('bounds').split(']')[0]
        position = position.replace("[", "").split(",")
        print("Testando APP")
        tap_screen(app_name, position[0], position[1])
    else:
        for n in node.findall('node'):
            open_app(n, app_name)


def get_apps():
    xml = ET.parse('window_dump.xml')
    root = xml.getroot()
    app = open_app(root, 'Play Store')


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

def inverting_colors():
    print("ENABLES")
    subprocess.Popen('adb shell settings put secure accessibility_display_inversion_enabled 1', shell=True, stdout=subprocess.PIPE)
    time.sleep(3)
    print("DISABLES")
    subprocess.Popen('adb shell settings put secure accessibility_display_inversion_enabled 0', shell=True, stdout=subprocess.PIPE)
    time.sleep(3)

def install_apps():
    print("INSTALANDO APKs")
    # swipe_screen()1
    time.sleep(2)
    output = subprocess.Popen("adb install ./apks/wikipedia.apk", shell=True, stdout=subprocess.PIPE)
    time.sleep(2)
    output = subprocess.Popen("adb install ./apks/ankidroid.apk", shell=True, stdout=subprocess.PIPE)
    time.sleep(3)

def uninstall_apps():
    print("DESINSTALANDO APKs")
    # swipe_screen()
    time.sleep(2)
    output = subprocess.Popen("adb uninstall org.wikipedia", shell=True, stdout=subprocess.PIPE)
    time.sleep(2)
    output = subprocess.Popen("adb uninstall com.ichi2.anki", shell=True, stdout=subprocess.PIPE)
    time.sleep(2)
    output = subprocess.Popen("adb shell input keyevent 4", shell=True, stdout=subprocess.PIPE)

device = get_devices()

