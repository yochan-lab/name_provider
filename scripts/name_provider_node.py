#!/usr/bin/env python

__author__ = 'daniel'

import rospy
#import roslib
#roslib.load_manifest('name_provider')
import pickle
import os.path

from std_msgs.msg import String, Int32

from name_provider.srv import *
from name_provider.msg import *
import rosplan_interface as interface

class Human(object):
    def __init__(self, input_name, input_id):
        self._person = Person()
        self._person.name = input_name
        self._person.id = input_id

    def __str__(self):
        return "<Human: %s, %d>" % (self._person.name, self._person.id)
        
    def get_message(self):
	return self._person

population = {}

def handle_get_real_name(req):
    if req.id in population:
        return {"name": population[req.id]._person.name,
                "found_name": True}
    else:
        return {"name": "",
                "found_name": False}


def handle_create_new_person(req):
    if req.name != "":
	rospy.loginfo("Creating %s with id %s" % (str(req.name) ,str(req.id)))
	human = Human(req.name, req.id)
	population[req.id] = human
	with open(pop_file, 'w') as file:
	    pickle.dump(population, file)
	interface.add_instance('person', human._person.name, human) 
	return True
    else:
	return False


if __name__ == '__main__':
    rospy.init_node("name_provider_node")
    interface.init()

    pop_file = '/home/yochan/names.pickle'
    if os.path.isfile(pop_file):
	with open(pop_file, 'r') as file:
	    population = pickle.load(file)

    for key in population:
	h = population[key]
	interface.add_instance('person', h._person.name, h) 

    get_name_service = rospy.Service("get_real_name", GetRealName, handle_get_real_name)
    get_name_service = rospy.Service("create_new_person", CreateNewPerson, handle_create_new_person)
    rospy.spin()
