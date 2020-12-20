#!python3

import paho.mqtt.client as mqtt #import the client1
import time
import os

###################
## env variables ##
###################

env_broker = os.environ['BROKER'] # static IP or localhost
env_user = os.environ['USERNAME']
env_pass = os.environ['PASSWORD']

##########################
## function definitions ##
##########################

def on_log(client, userdata, level, buf):
    print("log: "+buf)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected OK")
    else:
        print("Bad connection return code=", rc)

def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected result code " + str(rc))

def on_message(client, userdata, msg):
    m_decode = str(msg.payload.decode("utf-8"))
    print("message received", m_decode)
    print("message topic=", msg.topic)
    print("message qos", msg.qos)
    print("message retain flag=", msg.retain)

def get_cpu_temp():
    result = 0.0
    path = '/sys/class/thermal/thermal_zone0/temp'
    if os.path.isfile(path):
        with open(path) as f:
            line = f.readline().strip()
        if line.isdigit():
            result = float(line) / 1000
    return result


# tests
print("cpu temp: ", get_cpu_temp())

################
## mqtt setup ##
################

# init
client = mqtt.Client( "ruiner-stats" )
client.username_pw_set( env_user, env_pass )
client.on_connect=on_connect
client.on_disconnect=on_disconnect
client.on_log=on_log
client.on_message=on_message

# connect
print("connecting to broker ", env_broker)
client.connect(env_broker)
client.loop_start()

time.sleep(2)

# loop
while True:
    temperature = get_cpu_temp()
    ret = client.publish("ruiner/cpu/temperature", temperature, 0, True)
    print("publish return=", ret)
    time.sleep(60*5)

# disconnect
time.sleep(4)
print("Disconnecting from broker...")
client.loop_stop()
client.disconnect()