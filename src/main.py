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

env_qos = int(os.environ['QOS'])
env_cpu_temp_topic = os.environ['CPU_TEMP_TOPIC']

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

def on_publish(client,userdata,result):
    print("Data published ", result)

def get_cpu_temp():
    result = 0.0
    path = '/sys/class/thermal/thermal_zone0/temp'
    if os.path.isfile(path):
        with open(path) as f:
            line = f.readline().strip()
        if line.isdigit():
            result = float( int( float(line) / 100 ) / 10) # funky rounding to 000.0 format
    return result

#start
print("=== starting pi-sensors ===")

# tests
print("= tests =")
print("cpu temp: ", get_cpu_temp())
print("= tests complete =")

################
## mqtt setup ##
################

# init
print("= initialise mqtt =")
client = mqtt.Client( "ruiner-stats" )
client.username_pw_set( env_user, env_pass )
client.on_connect=on_connect
client.on_disconnect=on_disconnect
client.on_log=on_log
#client.on_publish=on_publish

# connect
print("connecting to broker ", env_broker)
client.connect(env_broker)
client.loop_start()

time.sleep(2)

# loop
print("= begin program loop =")
while True:
    temperature = get_cpu_temp()
    print("publishing ", env_cpu_temp_topic, " = ", temperature, " ...")
    client.publish(env_cpu_temp_topic, temperature, env_qos, True)
    time.sleep(60*5)

# disconnect
print("= begin program termination =")
time.sleep(4)
print("Disconnecting from broker...")
client.loop_stop()
client.disconnect()