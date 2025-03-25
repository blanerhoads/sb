#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pickle

class SetToucher:
    def __init__(self, elements_by_subset: dict):
        self.elements_by_subset = elements_by_subset.copy()
        self.subsets_by_element = dict()
        for subset, elements in elements_by_subset.items():
            for element in elements:
                if element not in self.subsets_by_element:
                    self.subsets_by_element[element] = set()
                self.subsets_by_element[element].add(subset)
        self.elements_remaining = set(self.subsets_by_element.keys())
    def __repr__(self):
        d = dict()
        #d["elements_by_subset"] = self.elements_by_subset
        #d["subsets_by_element"] = self.subsets_by_element
        #d["elements_remaining"] = self.elements_remaining
        d["n_elements_remaining"] = len(self.elements_remaining)
        # print in matrix form too?
        return d.__repr__()
    def touch(self, element: any):
        for subset in self.subsets_by_element[element]:
            if subset in self.elements_by_subset:
                self.elements_by_subset.pop(subset)
        self.subsets_by_element.pop(element)
    def touch_all(self):
        while len(self.elements_by_subset) > 0:
            key = lambda k: len(self.subsets_by_element[k])
            mode = max(self.subsets_by_element, key=key)
            print("Removing all", key(mode), "appearances of", mode)
            self.touch(mode)
            self.elements_remaining.remove(mode)

seqs = pickle.load(open("sheets.p", "rb"))
elements_by_subset = dict()
for i, seq in enumerate(seqs):
    elements_by_subset[i] = set()
    for pair in seq:
        elements_by_subset[i].add(pair)
#elements_by_subset = {10: {('a', , "b"}, 11: set("bc"), 12: set("cd")}
set_toucher = SetToucher(elements_by_subset)
set_toucher.touch_all()

d = dict()
for c, p in set_toucher.elements_remaining:
    if c not in d:
        d[c] = []
    d[c].append(p)
for c, prices in d.items():
    print(len(prices), c, prices)
print(len(set_toucher.elements_remaining), "total")
