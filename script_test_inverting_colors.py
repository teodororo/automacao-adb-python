import subprocess
import time

def record_screen():
    print("RECORDING SCREEN")
    subprocess.Popen("adb shell screenrecord --time-limit 5 /sdcard/DCIM/inverting_colors.mp4", shell=True, stdout=subprocess.PIPE)
    time.sleep(2)

def get_devices():
    output = subprocess.Popen('adb devices', shell=True, stdout=subprocess.PIPE).communicate()[0]
    output = str(output).split('attached')[1]
    output = output.split('device')[0]
    output = output.replace("\\n", "").replace("\\r", "")
    output = output.replace("\\t", "")
    return output

def inverting_colors():
    print("ENABLES")
    subprocess.Popen('adb shell settings put secure accessibility_display_inversion_enabled 1', shell=True, stdout=subprocess.PIPE)
    time.sleep(3)
    print("DISABLES")
    subprocess.Popen('adb shell settings put secure accessibility_display_inversion_enabled 0', shell=True, stdout=subprocess.PIPE)
    time.sleep(3)

def get_record(serial):
    time.sleep(5)
    print("PULLING .mp4")
    subprocess.Popen('adb -s %s pull /sdcard/DCIM/inverting_colors.mp4'%serial, shell=True, stdout=subprocess.PIPE)

record_screen()
device = get_devices()
inverting_colors()
get_record(device)
