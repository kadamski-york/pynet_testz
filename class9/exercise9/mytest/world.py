#!/usr/bin/env python

class MyClass(object):
    def __init__(self, building, room, jack):
        self.building = building
        self.room = room
        self.jack = jack

    def hello(self):
        print self.building+' '+self.room+' '+ self.jack

    def not_hello(self):
        print self.building
        print self.room
        print self.jack

class MyChildClass(MyClass):
    def hello(self):
        print 'Jack '+self.jack+' is in room '+self.room+' in building '+self.building

def func1():
    for i in range(3, 6):
        print i


if __name__ == "__main__":

    func1()

