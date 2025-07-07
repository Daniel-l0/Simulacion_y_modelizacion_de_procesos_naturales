#!/usr/bin/python
# -*- coding: latin-1 -*-

from heapq import *
from numpy import random

### STATE ##########################################

class State:
    def __init__(self):
        self.green = False
        self.cars = 0
    def is_green(self):
        return self.green
    def add_car(self):
        self.cars = self.cars + 1
    def purge_cars(self):
        self.cars = 0
    def waiting_cars(self):
        return self.cars
    def turn_green(self):
        self.green = True
    def turn_red(self):
        self.green = False
    def __str__(self):
        return "Green light =" + str(self.green) + ", cars=" + str(self.cars)

### EVENTS ###########################################

Tc = 30
Tp = 15  # <- CAMBIADO para la parte 2

class Event:
    def time(self):
        return self.t
    def __str__(self):
        return self.name + "(" + str(self.t) + ")"
    def __lt__(self, other):
        return self.t < other.t
    
class CAR(Event):
    def __init__(self, time):
        self.t = time
        self.name = "CAR"
    def action(self, queue, state):
        if not state.is_green():
            state.add_car()  # LINEA 77
            if state.waiting_cars() == 1:
                queue.insert(R2G(self.t + Tc))  # LINEA 79

class R2G(Event):
    def __init__(self, time):
        self.t = time
        self.name = "R2G"
    def action(self, queue, state):
        queue.insert(G2R(self.t + state.waiting_cars() * Tp))
        state.turn_green()  # LINEA 87
        state.purge_cars()

class G2R(Event):
    def __init__(self, time):
        self.t = time
        self.name = "G2R"
    def action(self, queue, state):
        state.turn_red()  # LINEA 95

### EVENT QUEUE ##############################################

class EventQueue:
    def __init__(self):
        self.q = []
    def notEmpty(self):
        return len(self.q) > 0
    def remaining(self):
        return len(self.q)
    def insert(self, event):
        heappush(self.q, event)
    def next(self):
        return heappop(self.q)

### MAIN #####################################################

Q = EventQueue()

# Eventos base
Q.insert(CAR(10))
Q.insert(CAR(25))
Q.insert(CAR(35))
Q.insert(CAR(60))
Q.insert(CAR(75))

# Parte 2: 100 autos aleatorios adicionales
random.seed(1)
additionalNumCarInQueue = 100
tRandom = 80
for i in range(1, additionalNumCarInQueue):
    tRandom = random.randint(tRandom+1, tRandom+10)
    Q.insert(CAR(tRandom))

S = State()

# Procesar eventos
last_event = None
while Q.notEmpty():
    e = Q.next()
    print(e)
    e.action(Q, S)
    last_event = e

print(f"\n✅ Último evento: {last_event}")


