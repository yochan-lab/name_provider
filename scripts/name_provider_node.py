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
        #add to rosplan
pop_file = '/home/yochan/names.pickle'
population = {}
if os.path.isfile(pop_file):
    with open(pop_file, 'r') as file:
	population = pickle.load(file)


def handle_get_real_name(req):
#    is_known_person = False
#    nombre = ""
    rospy.loginfo("Called name db %s" % str(req.id)) 

#     for p in population:
#         if p._person.id == req.id:
#             rospy.loginfo("%s %s %s" % ( str(p._person.id), str(req.id) , str(p._person.id == req.id)))
# 	    is_known_person = True
#             nombre = p._person.name
#             break

    if req.id in population:
	rospy.loginfo("surprise nom nom: %s" % str(population[req.id]._person.name))
	for keys, values in population.iteritems():
	    rospy.loginfo("key %s" % str(keys))
	    rospy.loginfo("value %s" % str(values))
        return {"name": population[req.id]._person.name,
                "found_name": True}
    else:
        return {"name": "",
                "found_name": False}


def handle_create_new_person(req):
#     if req.id in population:
# 	for p in population:
# 	    if p._person.id == req.id:
# 		p._person.name = req.name
# 		break
# 	return True
    if req.name != "":
	rospy.loginfo("Creating %s with id %s" % (str(req.name) ,str(req.id)))
	population[req.id] = Human(req.name, req.id)
	with open(pop_file, 'w') as file:
	    pickle.dump(population, file)
	return True
    else:
	return False

if __name__ == '__main__':
    rospy.init_node("name_provider_node")
    # interface.init()

    get_name_service = rospy.Service("get_real_name", GetRealName, handle_get_real_name)
    get_name_service = rospy.Service("create_new_person", CreateNewPerson, handle_create_new_person)
    rospy.spin()
