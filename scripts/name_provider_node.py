#!/usr/bin/env python

__author__ = 'daniel'

import rospy
#import roslib
#roslib.load_manifest('name_provider')

from std_msgs.msg import String, Int32

from name_provider.srv import *
from name_provider.msg import *
import rosplan_interface as interface

class Human(object):
    def __init__(self, input_name, input_id):
        self._person = Person
        self._person.name = input_name
        self._person.id = input_id

        #add to rosplan

population = []


def handle_get_real_name(req):
    is_known_person = False
    nombre = ""

    for p in population:
        if p._person.id == req.id:
            is_known_person = True
            nombre = p._person.name
            break

    if is_known_person:
        return {"name": nombre,
                "found_name": True}
    else:
        return {"name": "",
                "found_name": False}


def handle_create_new_person(req):
    if req.name != "":
	population.append(Human(req.name, req.id))
	return True
    else:
	return False

if __name__ == '__main__':
    rospy.init_node("name_provider_node")
    # interface.init()

    get_name_service = rospy.Service("get_real_name", GetRealName, handle_get_real_name)
    get_name_service = rospy.Service("create_new_person", CreateNewPerson, handle_create_new_person)
    rospy.spin()
