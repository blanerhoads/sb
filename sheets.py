#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import pickle
import random

class Configuration:
    def __init__(self, i_prices):
        self.categories = ["potent quotaBles", "famous fIrsts", "what's in a Name?", "ameriGo", "pOtpourri"]
        self.prices = [100 * (1 + i) for i in i_prices]
        self.pairs = [(category, price) for category in self.categories for price in self.prices]
    def __repr__(self):
        return self.pairs.__repr__()

configuration = Configuration(range(10))
print(configuration.pairs)

class Sheet:
    def __init__(self, configuration):
        self.df = pd.DataFrame(columns=list(configuration.categories))
        for category in configuration.categories:
            nr = min(5, len(configuration.prices))
            self.df[category] = random.sample(configuration.prices, nr)
            #self.df[category] = configuration.prices[:nr]
    def __str__(self):
        return self.df.to_string(index=False)
    def sequences(self):
        nr, nc = self.df.shape
        rows = [[] for _ in range(nr)]  # Not nr * [[]] because it makes references to the same list!
        cols = [[] for _ in range(nc)]
        diags = [[] for _ in range(2)]
        for ic in range(nc):
            for ir in range(nr):
                category = self.df.columns[ic]
                price = int(self.df.iloc[ir, ic])
                pair = (category, price)
                rows[ir].append(pair)
                cols[ic].append(pair)
                if nc == nr:
                    if ir == ic:
                        diags[0].append(pair)
                    if ir == nc - 1 - ic:
                        diags[1].append(pair)
        if nc == nr:
            return rows + cols + diags
        return rows + cols

sheets = []
for _ in range(10):
    sheets.append(Sheet(configuration))

for i, sheet in enumerate(sheets):
    print(sheet)
    sheet.df.to_csv(f"sheet_{i}.csv", index=False)

seqs = []
for sheet in sheets:
    seqs += sheet.sequences()
#print(seqs)
pickle.dump(seqs, open("sheets.p", "wb"))
