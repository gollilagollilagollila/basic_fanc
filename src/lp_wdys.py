#!/usr/bin/env python
# -*- cording: utf-8 -*-

# Language processing for 'What Did You Say'

import Levenshtein as lev
import fuzzy
import yaml

# [parameter]---------->
Threshold = 0.4    # 編集距離の閾値
# <---------------------

class Selector(object):
    def __init__(self, file_path):
        self.question = []
        self.answer = []

        self._dataLoader_(file_path)

    def _dataLoader_(self, file_path):
        file = open(file_path, 'r+')
        data = yaml.load(file, yaml.SafeLoader)

        for i, w in enumerate(data):
            self.question.append(w["q"])
            self.answer.append(w["a"])

    def __del__(self):
        pass

    def getDistance(self, base, target):
        phonetic_base = fuzzy.nysiis(base)
        phonetic_target = fuzzy.nysiis(target)
        return lev.distance(phonetic_base, phonetic_target)\
                /(max(len(phonetic_base), len(phonetic_target))* 1.00)

    def getDistanceList(self, sentence):
        distance_list = []
        for w in self.question:
            distance_list.append(self.getDistance(w, sentence))
        return distance_list

    def checker(self, sentence):
        distance_list = self.getDistanceList(sentence)
        closest_distance = min(distance_list)

        print(distance_list)
        if closest_distance >= Threshold:
            return [None, None]
        else:
            num = distance_list.index(closest_distance)
            return [self.question[num], self.answer[num]]
