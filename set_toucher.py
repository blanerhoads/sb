#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from game import Game
import numpy as np
import pickle
import random

class SetToucher:
    def __init__(self, game):
        self.squares_by_subset = dict()
        self.subsets_by_square = dict()
        for i, seq in enumerate(game.seqs):
            self.squares_by_subset[i] = set()
            for square in seq:
                self.squares_by_subset[i].add(square)
        for subset, squares in self.squares_by_subset.items():
            for square in squares:
                if square not in self.subsets_by_square:
                    self.subsets_by_square[square] = set()
                self.subsets_by_square[square].add(subset)
        #self.squares_remaining = set(self.subsets_by_square.keys())
        self.squares_remaining = set(game.squares)
        self.squares_removed = []
    def __repr__(self):
        d = dict()
        #d["squares_by_subset"] = self.squares_by_subset
        #d["subsets_by_square"] = self.subsets_by_square
        #d["squares_remaining"] = self.squares_remaining
        d["n_squares_remaining"] = len(self.squares_remaining)
        # print in matrix form too?
        return d.__repr__()
    def touch(self, square: any):
        for subset in self.subsets_by_square[square]:
            if subset in self.squares_by_subset:
                self.squares_by_subset.pop(subset)
        self.subsets_by_square.pop(square)
    def touch_all(self):
        while len(self.squares_by_subset) > 0:
            key = lambda k: len(self.subsets_by_square[k])
            mode = max(self.subsets_by_square, key=key)
            print(f"Removing all {key(mode)} appearances of {mode.q}")
            self.touch(mode)
            self.squares_remaining.remove(mode)
            self.squares_removed.append(mode)
        #exit(1)

#random.seed(42)

#n_min = 3
#for i_try in range(100):
game = Game(4, 3, n_squares=21, n_sheets=15)
game = pickle.load(open("game_n_min_1.pickle", "rb"))
print(game)
#for i_sheet, sheet in enumerate(game.sheets):
#   print(f"{sheet}\n\n\n")
    #print_choices(choices) # Manually include in doc with judges, rules, etc.

set_toucher = SetToucher(game)
#print(set_toucher.squares_by_subset)

set_toucher.touch_all()
choices = list(set_toucher.squares_remaining)
choices.sort(key=lambda s: s.category)
counts = dict()
def add_prices(choices):
    for square in choices:
        if square.category not in counts:
            counts[square.category] = 0
        counts[square.category] += 1
        square.price = counts[square.category] * 100
add_prices(choices)
print("\n\n\n")

def print_choices(choices, include_answers=False):
    for i, square in enumerate(choices):
        if square.category:
            #if square.category not in counts:
                #counts[square.category] = 0
            #counts[square.category] += 1
            print(f"({i + 1}) {square.category} for ${square.price}")
        if include_answers:
            print(f"\t{square.a}\n\t\t{square.prefix} {square.q}?")

print("\n\nChoices for players (to cross off as you go):\n")
print_choices(choices)

print("\n\nChoices for players (to cross off as you go), with answers and questions:\n")
print_choices(choices, include_answers=True)

set_toucher.squares_removed.sort(key=lambda s: s.category)
sorted_by_question = choices.copy()
sorted_by_question.sort(key=lambda s: s.q)
print("\n\nSame choices sorted by question (for judge to check off):\n")
for i, square in enumerate(sorted_by_question):
    print(f"({i + 1}) {square.q}")

print("\n\nAdditional choices for host to trigger blackout:\n")
add_prices(set_toucher.squares_removed)
print_choices(set_toucher.squares_removed, include_answers=True)

#n = len(set_toucher.squares_removed)
#if n < n_min:
#    n_min = n
#    pickle.dump(game, open(f"game_n_min_{n_min}.pickle", "wb"))
#    if n_min == 1:
#        break
