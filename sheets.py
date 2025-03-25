#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import pickle
import random

pd.set_option('display.max_columns', None)

class Square:
    def __init__(self, row):
        self.row = row
        self.prefix = row['prefix']
        self.q = row['q']
        self.a = row['a']
        self.category = row['category']
        self.price = row['price']
    def __repr__(self):
        return f"{self.prefix} {self.q}?"

class Sheet:
    def __init__(self, nr, nc, n_squares, squares):   # rm n_squares
        self.nr = nr
        self.nc = nc
        self.n_squares = n_squares
        self.squares = random.sample(squares, nr * nc)
        self.df = pd.DataFrame(np.array(self.squares).reshape(nr, nc), index=range(nr), columns=range(nc))
        self.seqs = self.sequences()
    def __str__(self):
        return self.df.to_string(index=False, header=False)
    def sequences(self):
        nr, nc = self.df.shape
        rows = [[] for _ in range(nr)]  # Not nr * [[]] because it makes references to the same list!
        cols = [[] for _ in range(nc)]
        diags = [[] for _ in range(2)]
        for ic in range(nc):
            for ir in range(nr):
                square = self.df.iloc[ir, ic]
                rows[ir].append(square)
                cols[ic].append(square)
                if nc == nr:
                    if ir == ic:
                        diags[0].append(square)
                    if ir == nc - 1 - ic:
                        diags[1].append(square)
        if nc == nr:
            return rows + cols + diags
        return rows + cols
    
class Game:
    def __init__(self, nr, nc, n_squares, n_sheets):
        self.nr = nr
        self.nc = nc
        self.n_squares = n_squares
        self.df_squares = pd.read_csv("df_squares.csv")
        self.squares = [Square(row) for _, row in self.df_squares.iterrows()]
        self.sheets = [Sheet(self.nr, self.nc, self.n_squares, self.squares) for _ in range(n_sheets)]
        self.seqs = [square for sheet in self.sheets for square in sheet.seqs]
    def __str__(self):
        s = ""
        for i, sheet in enumerate(self.sheets):
            s += f"Sheet {i}:\n\n" + str(sheet) + "\n\n"
        s += str(self.seqs)
        return s

game = Game(2, 2, 4, 12)

for i, sheet in enumerate(game.sheets):
    sheet.df.to_csv(f"sheet_{i}.csv", index=False)

pickle.dump(game.seqs, open("sheets.pickle", "wb"))
