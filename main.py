# import time
import os
import datetime  # Clock & Time
import requests  # Telegram
import paho.mqtt.client as mqtt  # MQTT

# MQTT Server
mqtt_user = "guy"
mqtt_password = "kupelu9e"
mqtt_address = "192.168.2.100"
mqtt_port = 1883

# Topics Subscribe:
subsTopics = {"myHome/Messages", "myHome/log", "myHome/debug"}

# log file
MAX_FILE_SIZE = 100
PATH = '/Users/guydvir/'
FILE_NAME = 'sublog'
FILE_EXT = 'txt'
FILE_SUFFIX_COUNTER = 0
filename = PATH + FILE_NAME + "_" + str(FILE_SUFFIX_COUNTER) + '.' + FILE_EXT  # topics.txt

# Telegram
chat_id = "596123373"
TELEGRAM_TOKENS = ["812406965:AAEaV-ONCIru8ePuisuMfm0ECygsm5adZHs",
                   "497268459:AAESYm27tJfNXwnnnn0slbmWnkqvbWgQEyw",
                   "1238925698:AAGWARuQ2eyx2i0ui2sCp_mM7xInTsKgUuM"]


def send_telegram_msg(message, to_id=0, char_id=chat_id):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKENS[to_id]}/sendMessage?chat_id={chat_id}&text={message}"
    print(requests.get(url).json())  # sends message to BOT


def gen_filename():
    filename = PATH + FILE_NAME + "_" + str(FILE_SUFFIX_COUNTER) + '.' + FILE_EXT  # topics.txt


def get_filesize(file=filename):
    file_stats = os.stat(file)
    print(file_stats.st_size)


def write2file(line, use_timestamp=False, newLine=True, file=filename):
    if newLine:
        line = line + "\n"
    with open(filename, 'a') as f:
        if not use_timestamp:
            f.write(line)
        else:
            f.write(msg_w_timestamp(line))


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connection to MQTT server {mqtt_address} succeeded")
    else:
        print(f"Connection to MQTT server {mqtt_address}failed. Result code {rc}")

    for _topic in subsTopics:
        client.subscribe(_topic)
        print(f"Subscribed: {_topic}")


def on_message(client, userdata, msg):
    _str = "[" + str(msg.topic) + "] -->" + str(msg.payload, "UTF-8")
    print(_str)
    write2file(_str, True, True)


def connect_mqtt_server():
    global client
    global mqtt_connected
    client = mqtt.Client("Python_terminal")
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(mqtt_user, mqtt_password)
    client.connect(mqtt_address, mqtt_port)
    mqtt_connected = client.is_connected()


def loop_mqtt():
    client.loop()


def msg_w_timestamp(msg):
    _msg = "[" + get_clk() + "]" + msg
    return _msg


def get_clk():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def all_loop():
    while True:
        loop_mqtt()


def start_msg():
    _str = "\n\n" + msg_w_timestamp(" ~~ Start ~~ ")
    write2file(_str, False, True)


if __name__ == "__main__":
    # start_msg()
    # connect_mqtt_server()
    # send_telegram_msg("hello")
    # all_loop()
    get_filesize()
