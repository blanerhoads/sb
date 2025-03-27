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
    def __init__(self, nr, nc, squares):
        self.nr = nr
        self.nc = nc
        self.squares = random.sample(squares, nr * nc)
        self.df = pd.DataFrame(np.array(self.squares).reshape(nr, nc), index=range(nr), columns=range(nc))
        self.seqs = self.sequences()
    def __str__(self):
        df = pd.DataFrame(index=range(self.nr * 2))
        for c in self.df.columns:
            df.loc[::2, c] = self.df[c].astype(str).str.ljust(35).values
        df.loc[1::2] = ""
        return df.to_string(index=False, header=False)
    def sequences(self):
        nr, nc = self.df.shape
        rows = [[] for _ in range(nr)]  # Not nr * [[]] because it makes references to the same list!
        cols = [[] for _ in range(nc)]
        diags = [[] for _ in range(2)]
        blackouts = [[]]
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
                blackouts[0].append(square)
        #print(f"rows: {rows}")
       # print(f"cols: {cols}")
        #print(self)
        #print(f"cols:\n\n{cols}\n\n\n")
        #print(f"blackouts: {blackouts}")
        #exit(1)
        #return cols
        return blackouts
        #if nc == nr:
            #return diags
            #return rows + cols + diags
        return rows + cols
    
class Game:
    def __init__(self, nr, nc, n_squares, n_sheets):
        self.nr = nr
        self.nc = nc
        self.df_squares = pd.read_csv("df_squares.csv")
        assert n_squares <= self.df_squares.shape[0]
        self.df_squares = self.df_squares.iloc[:n_squares, :]
        self.squares = [Square(row) for _, row in self.df_squares.iterrows()]
        self.sheets = [Sheet(self.nr, self.nc, self.squares) for _ in range(n_sheets)]
        self.seqs = [square for sheet in self.sheets for square in sheet.seqs]
    def __str__(self):
        s = ""
        for i, sheet in enumerate(self.sheets):
            #s += f"Sheet {i}:\n\n" + str(sheet) + "\n\n"
            s += f"\n\n" + str(sheet) + "\n\n"
        s += f"seqs: {str(self.seqs)}\n\n"
        #print(s)
        return s

game = Game(2, 2, n_squares=4, n_sheets=2)
print(game)
