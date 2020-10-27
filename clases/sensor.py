# import pigpio
# import DHT22
from time import sleep
# Initiate GPIO for pigpio

class dth22sensor:
    def __init__(self, pin):
        self.pin = pin
        pi = pigpio.pi()
        self.dht22 = DHT22.sensor(pi, pin)
    def readDHT22(self):
        # Get a new reading
        self.dht22.trigger()
        # Save our values
        humidity = '%.2f' % (self.dht22.humidity())
        temp = '%.2f' % (self.dht22.temperature())
        return (humidity, temp)
    def ejemplo(self):
        return self.pin