# import pigpio
# import DHT22
import time
import asyncio
import random
import mysql.connector
from BClima import mydb
# Initiate GPIO for pigpio

class dth22sensor:
    def __init__(self, pin):
        self.pin = pin
        #pi = pigpio.pi()
        #self.dht22 = DHT22.sensor(pi, pin)
    def readDHT22(self):
        # Get a new reading
        self.dht22.trigger()
        # Save our values
        humidity = '%.2f' % (self.dht22.humidity())
        temp = '%.2f' % (self.dht22.temperature())
        return (humidity, temp)
    def ejemplo(self):
        return self.pin
def asincTemHum():
    i=0
    j=0
    tot_humity = 0
    tot_temp = 0
    while True:
        i = i+1
        j += 1
        #pi = pigpio.pi()
        temp_or, humidity_or = getsensoraleatorio(True)
        #dht22 = DHT22.sensor(pi, pin)
        temp, humidity = getsensoraleatorio(False)
        print(f"{temp} {temp_or} dif {(temp - temp_or)} / {humidity} {humidity_or} dif{(humidity - humidity_or)}")
        tot_humity += humidity
        tot_temp += temp
        if(humidity_or - humidity) > 40:
            print('tiene humedad el servidor')
        if (temp_or - temp) > 40:
            print('esta sobrecalentandose')
        if temp_or > 70:
            print('el servidor se esta sobrcalentando y puede hacer que el sensor deje de funcionar a mas de 80')
        if humidity_or > 80:
            print('esta demaciado humedo revisa el entorno del servidor')
        if j == 50:
            try:
                cnx = mysql.connector.connect(**mydb)
                cur = cnx.cursor()
                try:
                    t_temp = tot_temp/50
                    t_hum = tot_humity/50
                    query = "INSERT INTO datosth (Idsensor, Temperatura, Humedad, Tiempo) VALUES (1, %s, %s, NOW());"%(t_temp, t_hum)
                    cur.execute(query)
                    cnx.commit()
                    j=0
                    tot_temp = 0
                    tot_humity = 0
                except Exception as e:
                    print(str(e))
                    break
                finally:
                    cur.close()
                    cnx.close()
            except Exception as e:
                print(str(e))
                break
        time.sleep(10)#espera 10 segundos

def getsensoraleatorio(ser):
    r1 = random.random()
    r2 = random.random()
    if(ser):
        temp = distribucion_normal(r1, 30, 80)
        hum = distribucion_normal(r2,0,100)
    else:
        temp = distribucion_normal(r1, -10, 50)
        hum = distribucion_normal(r2,0,100)
    return temp, hum

def distribucion_normal(numero, inicial, final):
    sumatoria = 0
    for i in range(12):
        sumatoria += (i*numero)-6
    #media
    media = (inicial+final)/2
    #varianza
    varianza = 0.275
    x = media + (varianza*sumatoria)
    return x