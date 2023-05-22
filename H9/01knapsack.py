# knapsack.py
# From Classic Computer Science Problems in Python Chapter 9
# Copyright 2018 David Kopec
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import NamedTuple, List


class Item(NamedTuple):
    name: str
    weight: int
    value: float


def knapsack(items: List[Item], max_capacity: int) -> List[Item]:
    # initialize dynamic programming table
    benefit = [[0.0 for _ in range(max_capacity + 1)] for _ in range(len(items) + 1)]
    """ Data Structures & Algorithms in Java, First Ed., p. 508
        Michael T. Goodrich & Roberto Tamassia
    """
    # dynamic programming on the benefit function value(k, w): k = item (offset by 1!), w = weight of item
    for k in range(1, len(items) + 1):
        for w in range(max_capacity + 1):
            wk = items[k - 1].weight
            """
            1. if the weight of the item currently under inspection exceeds the
               current capacity considered, it does not fit and this is the same
               situation as the previous item considered (previous row).
            2. item does fit within current capacity considered, take it if it
               maximizes the benefit
            """
            if wk > w:
                benefit[k][w] = benefit[k - 1][w]                                       # 1
            else:
                benefit[k][w] = max(
                    benefit[k - 1][w], benefit[k - 1][w - wk] + items[k - 1].value      # 2
                )

    solution: List[Item] = []
    capacity = max_capacity
    for i in range(len(items), 0, -1):  # work backwards
        # was this item used?
        if benefit[i - 1][capacity] != benefit[i][capacity]:
            solution.append(items[i - 1])
            # if the item was used, remove its weight
            capacity -= items[i - 1].weight
    return solution


if __name__ == "__main__":
    items: List[Item] = [
        Item("television", 50, 500),
        Item("candlesticks", 2, 300),
        Item("stereo", 35, 400),
        Item("food", 15, 50),
        Item("clothing", 20, 800),
        Item("jewelry", 1, 4000),
        Item("books", 100, 300),
        Item("printer", 18, 30),
        Item("refrigerator", 200, 700),
        Item("laptop", 3, 1000),
        Item("painting", 10, 1000),
    ]
    print(knapsack(items, 75))
