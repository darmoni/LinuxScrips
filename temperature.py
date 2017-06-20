#!/usr/bin/env python3

class Celsius:
    def __init__(self, temperature = 0):
        self._temperature = temperature

    def to_fahrenheit(self):
        return (self._temperature * 1.8) + 32

    def get_temperature(self):
        print("Getting value"),
        return self._temperature
    def set_temperature(self, value):
        if value < -273:
            raise ValueError("Temperature below -273.15 is not possible")
        print("Setting value")
        self._temperature = value
    temperature = property(get_temperature,set_temperature)

class Kelvin(Celsius):
    def set_temperature(self, value):
        if value < 0:
            raise ValueError("Temperature below 0 is not possible")
        print("Setting value")
        self._temperature = value
    def to_rankine(self):
            return self._temperature* 1.8
    temperature = property(Celsius.get_temperature,set_temperature)

class Rankine(Celsius):
    def to_fahrenheit(self):
        return self._temperature - 459.67
    def set_temperature(self, value):
        if value < 0:
            raise ValueError("Temperature below 0 is not possible")
        print("Setting value")
        self._temperature = value
    temperature = property(Celsius.get_temperature,set_temperature)

print ("Celsius(100)")
c = Celsius(100);
k = Kelvin(c.temperature+273.15)
r = Rankine(k.to_rankine());

print (c.temperature),
print (c.to_fahrenheit(), k._temperature, r.temperature, r.to_fahrenheit())

print ("Celsius(0)")
c.temperature = 0
k = Kelvin(c.temperature+273.15)
print (c.temperature),
print (c.to_fahrenheit(), k._temperature, k.to_rankine())

r = Rankine(k.to_rankine());

#print (r._temperature, r.to_fahrenheit())

print ("Celsius(-40)")
c.temperature = -40
k = Kelvin(c.temperature+273.15)
print (c.temperature),
print (c.to_fahrenheit(), k._temperature, k.to_rankine())

print ("Rankine(0)")
r.temperature = 0
print (r._temperature, r.to_fahrenheit())

print ("Rankine(459.67)")
r.temperature = 459.67
c.temperature = ((r.to_fahrenheit()-32)/1.8)
k = Kelvin(c.temperature+273.15)
print (c.temperature, k.temperature,r._temperature, r.to_fahrenheit())

