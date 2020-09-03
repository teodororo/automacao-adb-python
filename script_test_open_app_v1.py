'''
    Algoritmo script_test_open_app_v1.py
    Autores: Diego Torres, Giovanna S. Teodoro e João Guilherme S. Gomes
    Descrição: O algoritmo automatiza uma série de comandos adb (android debug bridge) que realizam em um device (os testes foram
               realizados em um emulador android pixel 3 com Android 9) a operação de abertura de um determinado app (no caso a
               Play Store).
    OBS: a numeração no início de cada descrição de função representa a ordem de execução das funções.
'''
import subprocess
import xml.etree.ElementTree as ET
import time
'''
    1 - A função get_devices() executa o comando adb devices, que listar todos os dispositivos conectados, então a saída é armazenada
        dentro da variavel output e na sequencia vão sendo aplicados alguns comandos para remover caracteres especiais como quebra de 
        linha e tabs para que no final venha somente o SERIAL do dispositivo conectado.
'''
def get_devices():
    output = subprocess.Popen('adb devices', shell=True, stdout=subprocess.PIPE).communicate()[0]
    output = str(output).split('attached')[1]
    output = output.split('device')[0]
    output = output.replace("\\n", "").replace("\\r", "")
    output = output.replace("\\t", "")
    return output
'''
    2 - A função get_screen() roda o comando adb shell uiatomator dump, que gera um xml com as posições do icones na tela, uma vez que 
        esse xml foi gerado ele é copiado para o diretorio onde está sendo executado o script com o comando adb pull.
'''
def get_screen(serial):
    output = subprocess.Popen('adb -s %s shell uiautomator dump'%serial,shell=True,stdout=subprocess.PIPE).communicate()[0]
    print(output)
    output = subprocess.Popen('adb -s %s pull /sdcard/window_dump.xml'%serial,shell=True,stdout=subprocess.PIPE).communicate()[0]
    print(output)
'''
    5 - A função tap_screen() recebe como parâmetros, o nome do aplicativo somente para que seja informado o nome na tela e as posições
        x e y do botão, essas posição são passadas para o comando adb shell input tap que vai clicar no app determinado (Play Store no 
        caso), como esse app demora para abrir é aguardado o tempo de 5 segundos e depois é executado o comando adb shell input keyvent 4,
        que é o equivalente ao botão voltar do android, então é voltado para a tela anterior.
'''
def tap_screen(app_name, x, y):
    print("Abrindo %s" % app_name)
    output = subprocess.Popen("adb shell input tap %s %s" % (x, y), shell=True, stdout=subprocess.PIPE)
    time.sleep(5)
    print("Voltando a tela anterior")
    output = subprocess.Popen("adb shell input keyevent 4", shell=True, stdout=subprocess.PIPE)
'''
    4 - A função test_app() verifica se o elemento atual do xml possui um atributo chamado text e se esse atributo é igual ao nome do app 
        procurado, que no caso é Play Store, caso esse app não seja encontrado é realizado um for buscando os elementos filhos do elemento 
        atual, fazendo assim uma recursividade até que sejam percorridos todos os elementos filhos desse xml. Quando o APP é encontrado, é
        pegado o valor do atributo bounds que guarda a posição do item na tela, essa posição é armazenada na variável position e depois é 
        chamada a função tap_screen que realizará o 'click' no botão.    
'''
def test_app(node, app_name):
    if node.attrib.get('text') == app_name:
        position = node.attrib.get('bounds').split(']')[0]
        position = position.replace("[", "").split(",")
        print("Testando APP")
        tap_screen(app_name, position[0], position[1])
    else:
        for n in node.findall('node'):
            test_app(n, app_name)
'''
    3 - A função get_apps() lê o arquivo xml gerado pelo adb faz o parse dele de string para xml e manda para a função test_app().
'''
def get_apps():
    xml = ET.parse('window_dump.xml')
    root = xml.getroot()
    app = test_app(root, 'Play Store')


device = get_devices()
get_screen(device)
get_apps()