#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class SetToucher:
    def __init__(self, elements_by_subset: dict):
        self.elements_by_subset = elements_by_subset.copy()
        self.subsets_by_element = dict()
        for subset, elements in elements_by_subset.items():
            for element in elements:
                if element not in self.subsets_by_element:
                    self.subsets_by_element[element] = set()
                self.subsets_by_element[element].add(subset)
    def __repr__(self):
        d = dict()
        d["elements_by_subset"] = self.elements_by_subset
        d["subsets_by_element"] = self.subsets_by_element
        # print in matrix form too?
        return d.__repr__()
    def touch(self, element: any):
        for subset in self.subsets_by_element[element]:
            if subset in self.elements_by_subset:
                self.elements_by_subset.pop(subset)
        self.subsets_by_element.pop(element)
    def touch_all(self):
        while len(self.elements_by_subset) > 0:
            most_frequent_element = max(self.subsets_by_element, key=lambda k: len(self.subsets_by_element[k]))
            print("\nmost_frequent_element", most_frequent_element)
            self.touch(most_frequent_element)
            print(self)

elements_by_subset = {10: set("abc"), 11: set("bc"), 12: set("bcd")}
set_toucher = SetToucher(elements_by_subset)
print(set_toucher)
set_toucher.touch_all()
