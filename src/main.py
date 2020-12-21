#!python3

#############
## imports ##
#############

import paho.mqtt.client as mqtt # 1.5.1
import psutil # 5.8.0

import time
import os

##########################
## function definitions ##
##########################
# mqtt functions
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

# helper getter functions
def get_cpu_temp():
    result = 0.0
    path = '/sys/class/thermal/thermal_zone0/temp'
    if os.path.isfile(path):
        with open(path) as f:
            line = f.readline().strip()
        if line.isdigit():
            result = round( (float(line) / 1000), 1 )
    return result

def get_cpu_use_total():
    return round( sum(psutil.cpu_percent(None, True)), 1)
def get_cpu_use_average():
    return round( psutil.cpu_percent(None, False), 1)
def get_cpu_use_for_core(i=0):
    cores = psutil.cpu_percent(None, True)
    if i < len(cores):
        return round( cores[i], 1 )
    else:
        return 0.0

def get_mem_total():
    return int( psutil.virtual_memory()[0] / (1024 ** 2) )
def get_mem_free():
    return int( psutil.virtual_memory()[1] / (1024 ** 2) )
def get_mem_percent():
    return round( float(psutil.virtual_memory()[2]), 1 )
def get_mem_use():
    return int( psutil.virtual_memory()[3] / (1024 ** 2) )

####################
## function tests ##
####################

print("=== tests ===")
# cpu
print("cpu temp:", get_cpu_temp())
print("cpu details:", psutil.sensors_temperatures())
print("cpu use:", psutil.cpu_percent())
print("cpu intel:", psutil.cpu_percent(None, True))
print("cpu intel2:", psutil.cpu_percent(None, False))
print("cpu total:", get_cpu_use_total())
print("cpu average:", get_cpu_use_average())
print("cpu 0:", get_cpu_use_for_core(0))
print("cpu 1:", get_cpu_use_for_core(1))
print("cpu 2:", get_cpu_use_for_core(2))
print("cpu 3:", get_cpu_use_for_core(3))
print("cpu 4:", get_cpu_use_for_core(4))
# memory
print("ram totl:", get_mem_total(), "MB")
print("ram free:", get_mem_free(), "MB")
print("ram used:", get_mem_use(), "MB")
print("ram perc:", get_mem_percent(), "%")
#disk
#   todo
print("=== tests complete ===")

#==========###############################==========#
#==========######### PI SENSORS ##########==========#
#==========###############################==========#
#start
print("=== starting pi-sensors ===")

###################
## env variables ##
###################

env_broker = os.environ['BROKER'] # static IP or localhost
env_user = os.environ['USERNAME']
env_pass = os.environ['PASSWORD']
env_qos = int(os.environ['QOS'])

env_cpu_temp_topic = os.environ['CPU_TEMP_TOPIC']
env_cpu_use_topic = os.environ['CPU_USE_TOPIC']

env_mem_total_topic = os.environ['MEM_TOTAL_TOPIC']
env_mem_free_topic = os.environ['MEM_FREE_TOPIC']
env_mem_use_topic = os.environ['MEM_USE_TOPIC']
env_mem_percent_topic = os.environ['MEM_PERCENT_TOPIC']

#######################
## mqtt setup & core ##
#######################
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

####################
## mqtt core loop ##
####################
print("= begin program loop =")
while True:
    ### cpu ###
    # cpu temp
    topic = env_cpu_temp_topic
    data = get_cpu_temp()
    print("> publishing:", topic, "=", data, " ...")
    client.publish(topic, data, env_qos, True)

    ### mem ###
    # mem total
    topic = env_mem_total_topic
    data = get_mem_total()
    print("> publishing ", topic, " = ", data, " ...")
    client.publish(topic, data, env_qos, True)
    # mem free
    topic = env_mem_free_topic
    data = get_mem_free()
    print("> publishing ", topic, " = ", data, " ...")
    client.publish(topic, data, env_qos, True)
    # mem use
    topic = env_mem_use_topic
    data = get_mem_use()
    print("> publishing ", topic, " = ", data, " ...")
    client.publish(topic, data, env_qos, True)
    # mem percent
    topic = env_mem_percent_topic
    data = get_mem_percent()
    print("> publishing ", topic, " = ", data, " ...")
    client.publish(topic, data, env_qos, True)

    ### storage ###
    # todo

    ### sleep ###
    time.sleep(60*5)

####################
## mqtt terminate ##
####################
# disconnect
print("= begin program termination =")
time.sleep(4)
print("Disconnecting from broker...")
client.loop_stop()
client.disconnect()
print("=== pi-sensors terminated ===")
