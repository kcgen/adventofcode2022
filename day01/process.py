#!/bin/env python3

# Copyright (C) 2022-2022  kcgen <kcgen@users.noreply.github.com>
# SPDX-License-Identifier: GPL-3.0-or-later

"""
--- Day 1: Calorie Counting ---

Santa's reindeer typically eat regular reindeer food, but they need a
lot of magical energy to deliver presents on Christmas. For that,
their favorite snack is a special type of star fruit that only grows
deep in the jungle. The Elves have brought you on their annual
expedition to the grove where the fruit grows.

To supply enough magical energy, the expedition needs to retrieve a
minimum of fifty stars by December 25th. Although the Elves assure you
that the grove has plenty of fruit, you decide to grab any fruit you
see along the way, just in case.

Collect stars by solving puzzles. Two puzzles will be made available
on each day in the Advent calendar; the second puzzle is unlocked when
you complete the first. Each puzzle grants one star. Good luck!

The jungle must be too overgrown and difficult to navigate in vehicles
or access from the air; the Elves' expedition traditionally goes on
foot. As your boats approach land, the Elves begin taking inventory of
their supplies. One important consideration is food - in particular,
the number of Calories each Elf is carrying (your puzzle input).

The Elves take turns writing down the number of Calories contained by
the various meals, snacks, rations, etc. that they've brought with
them, one item per line. Each Elf separates their own inventory from
the previous Elf's inventory (if any) by a blank line.

For example, suppose the Elves finish writing their items' Calories
and end up with the following list:

1000
2000
3000

4000

5000
6000

7000
8000
9000

10000

This list represents the Calories of the food carried by five Elves:

    The first Elf is carrying food with 1000, 2000, and 3000
    Calories, a total of 6000 Calories.

    The second Elf is carrying one food item with 4000 Calories.

    The third Elf is carrying food with 5000 and 6000 Calories, a
    total of 11000 Calories.

    The fourth Elf is carrying food with 7000, 8000, and 9000
    Calories, a total of 24000 Calories.

    The fifth Elf is carrying one food item with 10000 Calories.

In case the Elves get hungry and need extra snacks, they need to know
which Elf to ask: they'd like to know how many Calories are being
carried by the Elf carrying the most Calories. In the example above,
this is 24000 (carried by the fourth Elf).

Find the Elf carrying the most Calories. How many total Calories is
that Elf carrying?

"""

import argparse, pathlib
import sys
from dataclasses import dataclass


@dataclass
class Elf:
    id: int = 0
    total_cals: int = 0

    def AddCals(self, cals):
        self.total_cals += cals

    def __lt__(self, other):
        return self.total_cals < other.total_cals

    def __add__(self, other):
        ids = self.id + [other.id] if isinstance(self.id, list) else [self.id, other.id]
        total_cals = self.total_cals + other.total_cals
        return Elf(ids, total_cals)

    def __radd__(self, other):
        return self if other == 0 else self.__add__(other)


class TopN:
    items = list()

    def __init__(self, n_items, init_item):
        self.items = [init_item for i in range(n_items)]

    def Consider(self, candidate):
        for i in range(len(self.items)):
            if self.items[i] < candidate:
                self.items.insert(i, candidate)
                self.items.pop()
                break


def get_next_elf(elf) -> Elf:
    return Elf(id=elf.id + 1)


def process_list(items, n) -> Elf:
    elf = Elf(id=1)
    top_n = TopN(n, Elf(id=0))

    for item in items:
        if item.strip().isdigit():
            elf.AddCals(int(item))
        else:
            top_n.Consider(elf)
            elf = get_next_elf(elf)

    return top_n


def parse_args():
    parser = argparse.ArgumentParser(
        description="Find the Elf holding the most calories (Advent of Code: Day 1)"
    )
    parser.add_argument(
        "calories_file",
        metavar="FILE",
        type=pathlib.Path,
        help="A file holding zero or more calorie lists. One calorie per line."
        "A blank lines terminate the given elf's list.",
    )
    parser.add_argument(
        "top_n",
        metavar="N",
        type=int,
        choices=range(1, 100),
        help="Return the combined calories held by the top N elves.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    with args.calories_file.open("r") as items:
        top_n = process_list(items, args.top_n)

        print(f"Top {args.top_n} elves:")
        for elf in top_n.items:
            print("    ", elf)

        print(f"\nCombined:", sum(top_n.items))

    return 0


if __name__ == "__main__":
    sys.exit(main())
