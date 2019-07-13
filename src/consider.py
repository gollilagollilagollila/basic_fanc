#!/usr/bin/env python
# -*- cording: utf-8 -*-

import Levenshtein as lev

"""picospeakerを使うため"""
import subprocess

# [parameter]---------->
Threshold = 0.6    # 認識結果の閾値
# <---------------------


question_list = [   "which city are we in",\
                    "what is the name of your team",\
                    "what is the highest mountain in Japan",\
                    "what's your team's home city",\
                    "who created Star Wars",\
                    "who lives in a pineapple under the sea",\
                    "do you think robots are a threat to humanity",\
                    "who created the Python Programming Language",\
                    "who created the C Programming Language",\
                    "what is a chatbot"]

answer_list = [     "Kanazawa",\
                    "KIT Happy Robot",\
                    "Mount Fuji",\
                    "Kanazawa",\
                    "George Lucas",\
                    "Sponge Bob Squarepants!",\
                    "No. Humans are the real threat to humanity.",\
                    "Python was invented by Guido van Rossum.",\
                    "C was invented by Dennis MacAlistair Ritchie.",\
                    "A chatbot is an A.I. you put in customer service to avoid paying salaries."]

class distance(object):
    def __init__(self):
        global question_list
        global answer_list

        self.question = question_list
        self.answer = answer_list

    def check(self, string):
        result_final = 1.0
        list_num = 0

        for question in self.question:
             result = lev.distance(string, question)/(max(len(string), len(question)) *1.00)
             #print(result)
             if result_final >= result:
                 result_final = result
                 list_num = self.question.index(question)


        if result_final <= Threshold:
            self.speak(self.answer[list_num])
            return True
        else:
            self.speak("One more time please")
            return False

    def speak(self, sentense):
        print(sentense)
        voice_cmd = '/usr/bin/picospeaker -r -18 -p 3 %s' %sentense
        subprocess.call(voice_cmd.strip().split(' '))
