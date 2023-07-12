################################################################################################ 
####################################### CLIENTE MQTT ########################################### 
################################################################################################

from paho.mqtt import client as mqtt_client
from email.message import EmailMessage
import time
import random
import json
import ssl
import smtplib

def enviar_email(cont):
    email_emisor = 'leninalomoto2003@gmail.com'
    email_password = 'eatzjaetfuwqevhu'
    email_receptor = 'leninalomoto2003@gmail.com'

    asunto = 'multiplos de 10'
    cuerpo = 'el contador ha alcanzado un multiplo de 10, el numero es: ' + str(cont) 

    em = EmailMessage()
    em['From'] = email_emisor
    em['To'] = email_receptor
    em['Subject'] = asunto
    em.set_content(cuerpo)

    contexto = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=contexto) as smtp:
        smtp.login(email_emisor, email_password)
        smtp.sendmail(email_emisor, email_receptor, em.as_string())


#Hive
BROKER = 'broker.hivemq.com'
PORT = 1883
TOPIC_DATA = "cliente1"
TOPIC_ALERT = "cliente2"
# generate client ID with pub prefix randomly
CLIENT_ID = "python-mqtt-tcp-pub-sub-{id}".format(id=random.randint(0, 1000))
FLAG_CONNECTED = 0


def on_connect(client, userdata, flags, rc):
    global FLAG_CONNECTED
    global FLAG_CONNECTED
    if rc == 0:
        FLAG_CONNECTED = 1
        print("Connected to MQTT Broker!")
        client.subscribe(TOPIC_DATA)
        client.subscribe(TOPIC_ALERT)
    else:
        print("Failed to connect, return code {rc}".format(rc=rc), )


def on_message(client, userdata, msg):
    #print("Received `{payload}` from `{topic}` topic".format(payload=msg.payload.decode(), 
    #topic=msg.topic))
    try:
        print("Received `{payload}` from `{topic}` topic".format(payload=msg.payload.decode(), 
        topic=msg.topic))
        publish(client,TOPIC_ALERT,msg)               

    except Exception as e:
        print(e)

def connect_mqtt():
    client = mqtt_client.Client(CLIENT_ID)
    #client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT)
    return client

#Enviar mensajes
def publish(client,TOPIC,msg): 
    msg = json.dumps(msg)
    result = client.publish(TOPIC, msg)


client = connect_mqtt()
def run():
    cont = 1
    while True:
        publish(client, TOPIC_ALERT, cont)
        cont = cont + 1
        if cont % 10 == 0:
            enviar_email(cont)
        client.loop_start()
        time.sleep(1)
        if FLAG_CONNECTED:
            print("Wait for message...")
        else:
            client.loop_stop()


if __name__ == '__main__':
    run()