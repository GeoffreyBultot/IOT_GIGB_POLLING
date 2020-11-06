import sys
import time
import json
import paho.mqtt.client as mqtt


THE_BROKER = "eu.thethings.network"
THE_TOPIC = "+/devices/+/up"
lastmsg = []
currentmsg = []
# TTN_USERNAME is the Application ID
TTN_USERNAME = "gigb_iot_zone1"
TTN_PASSWORD = "ttn-account-v2.jd-xedDg0gEL_MJK__yxCYZ8IDa2FenUdtRZXOO7ndQ"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected to ", client._host, "port: ", client._port)
	print("Flags: ", flags, "return code: ", rc)
	
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe(THE_TOPIC)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	global lastmsg
	global currentmsg
	if(currentmsg != []):
		lastmsg = currentmsg
		currentmsg = json.loads(msg.payload.decode("utf-8"))
		#print(currentmsg["counter"] )
		if(lastmsg["counter"] != currentmsg["counter"] ):
			payload_fields = lastmsg["payload_fields"]
			#print(payload_fields)
			#print(payload_fields['luminosity'])
			#print(payload_fields['temperature'])
			luminosity = payload_fields['luminosity']
			temperature = payload_fields['temperature']
			
			dev_id = lastmsg["dev_id"]
			gtw_id = lastmsg["metadata"]["gateways"][0]["gtw_id"]
			rssi = lastmsg["metadata"]["gateways"][0]["rssi"]
			#print("%s, gtw=%s, rssi=%d" % (dev_id, gtw_id, rssi))
			if(dev_id == "arduino_mkrwan1300_gi"):
			   print("TRYHARD 1 A DIT : @%s >> temp=%.3f lux=%.3f" % (time.strftime("%H:%M:%S"), temperature, luminosity))		  
			elif(dev_id == "arduino_mdrwan1300_zone1"):
			   print("TRYHARD 2 A DIT : @%s >> temp=%.3f lux=%.3f" % (time.strftime("%H:%M:%S"), temperature, luminosity))		  
	else:
	  currentmsg = json.loads(msg.payload.decode("utf-8"))

client = mqtt.Client()

# Let's see if you inserted the required data
if __name__ == '__main__':
	if TTN_USERNAME == 'VOID':
		print("You must set the values of your app and device first!!")
		sys.exit()
	else:
		client.username_pw_set(TTN_USERNAME, password=TTN_PASSWORD)

		client.on_connect = on_connect
		client.on_message = on_message
		
		client.connect(THE_BROKER, 1883, 60)
				
		client.loop_forever()

