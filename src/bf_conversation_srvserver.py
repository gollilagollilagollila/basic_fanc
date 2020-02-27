#!/usr/bin/env python
#-*- coding: utf-8 -*-

import roslib
import rospy
from voice_common_pkg.srv import *

import lp_wdys


tts_pub = rospy.ServiceProxy('/tts', TTS)
stt_pub = rospy.ServiceProxy('/speech_recog', SpeechRecog)

file_name = "rcj2019_whatdidyousay_questions.yaml"
file_path = roslib.packages.get_pkg_dir("basic_fanc") + "/config/" + file_name
lp = lp_wdys.Selector(file_path)


def speak(sentence):
    tts_pub(sentence)
    return

def speechRecog():
    return stt_pub()

def conversation(_dammy):
    ros_response = WhatDidYouSayResponse()

    # recognition result
    sentence = speechRecog()
    print(sentence)
    result_list = lp.checker(sentence.result)

    if all(result_list):
        speak("Question is")
        speak(result_list[0])
        speak("Answer is")
        speak(result_list[1])
        ros_response.result = True
    else:
        speak("Sorry I couldn't be recognized")
        ros_response.result = False

    return ros_response

def rosConfig():
    rospy.init_node('bf_conversation_srvserver')
    rospy.Service('/bf/conversation_srvserver', WhatDidYouSay, conversation)
    rospy.loginfo('Ready to  conversation_srvserver')
    rospy.spin()

if __name__ == '__main__':
    rosConfig()
