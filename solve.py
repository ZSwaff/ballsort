#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import collections
import copy
import enum
import heapq
import itertools
import random


COLOR_SENTINEL = object()
aqua = blue = brown = gray = green = lime = orange = pink = purple = red = sky = yellow = COLOR_SENTINEL
Color = enum.Enum('Color', [k for k, v in locals().items() if v is COLOR_SENTINEL and k != 'COLOR_SENTINEL'])
locals().update({e.name: e for e in Color})
mx_color_len = max(len(e.name) for e in Color)


class PriorityQueue:
    def __init__(self):
        self.__heap = []
        self.__counter = itertools.count()

    def __len__(self):
        return len(self.__heap)

    def push(self, item, priority):
        heapq.heappush(self.__heap, (priority, next(self.__counter), item))

    def pop(self):
        return heapq.heappop(self.__heap)[2]


class Stack:
    def __init__(self):
        self.__heap = []

    def __len__(self):
        return len(self.__heap)

    def push(self, item, priority):
        self.__heap.append(item)

    def pop(self):
        return self.__heap.pop()


class Move:
    def __init__(self, color, init, final):
        self.color = color
        self.init = init
        self.final = final

    def __repr__(self):
        return f'{self.color} from {self.init + 1} to {self.final + 1}'


class Layout:
    @staticmethod
    def random(n_colors):
        balls = [Color(i) for i in range(1, n_colors + 1)] * 4
        random.shuffle(balls)
        return Layout.from_level_detail([balls[i * 4:(i + 1) * 4] for i in range(len(balls) // 4)])

    @staticmethod
    def from_level_detail(level_detail):
        assert all(len(e) == 4 for e in level_detail)
        assert all(e == 4 for e in collections.Counter(f for e in level_detail for f in e).values())

        buckets = dict(enumerate(level_detail))
        buckets.update({len(level_detail): [], len(level_detail) + 1: []})
        return Layout(buckets)

    def __init__(self, buckets):
        self.buckets = buckets

        self.n_buckets = len(buckets)
        self.n_colors = self.n_buckets - 2
        self.hash = hash(tuple(sorted(tuple(e.value for e in self.buckets[i]) for i in range(self.n_buckets))))
        self.is_organized = all(len(set(e)) <= 1 for e in self.buckets.values())

    def __hash__(self):
        return self.hash

    def __eq__(self, other):
        return self.hash == other.hash

    def __repr__(self):
        return '\n'.join(
            f'{i + 1:>3}. ' + ' '.join(f'{e.name:<{mx_color_len}}' for e in self.buckets[i])
            for i in range(self.n_buckets)
        )

    def get_moves_and_resulting_layouts(self):
        res = []
        for i_buck in range(self.n_buckets):
            if len(self.buckets[i_buck]) == 0:
                continue
            i_col = self.buckets[i_buck][-1]
            for f_buck in range(self.n_buckets):
                if f_buck == i_buck or len(self.buckets[f_buck]) == 4:
                    continue
                if len(self.buckets[f_buck]) != 0 and self.buckets[f_buck][-1] != i_col:
                    continue
                # this is going to be the slowest part
                n_bucks = copy.copy(self.buckets)
                n_bucks[i_buck] = copy.copy(n_bucks[i_buck])
                n_bucks[f_buck] = copy.copy(n_bucks[f_buck])
                n_bucks[f_buck].append(n_bucks[i_buck].pop())
                res.append((Move(i_col.name, i_buck, f_buck), Layout(n_bucks)))
        random.shuffle(res)
        return res

    def get_dist_to_organized_heuristic(self):
        # could improve this heuristic
        # right now it assumes you could directly move all balls of a color to the tube with the max of that color
        return sum(4 - max(len([f == i for f in e]) for e in self.buckets.values()) for i in range(self.n_colors))


class SearchState:
    def __init__(self, layout, parent, move, dist):
        self.layout = layout
        self.parent = parent
        self.move = move
        self.dist = dist

    def __hash__(self):
        return hash(self.layout)

    def __eq__(self, other):
        return self.layout == other.layout

    def is_valid(self):
        return True

    def is_finished(self):
        return self.layout.is_organized

    def get_neighbors(self):
        return [SearchState(f, self, e, self.dist + 1) for e, f in self.layout.get_moves_and_resulting_layouts()]

    def get_dist_from_start(self):
        return self.dist

    def get_dist_to_finish_heuristic(self):
        # this would be where we would return a different heuristic if we don't have full visibility
        # just returning 0 would be naive in that case because we could remember what we have seen
        return self.layout.get_dist_to_organized_heuristic()


def search(start, optimal):
    if optimal:
        q = PriorityQueue()
    else:
        q = Stack()
    q.push(start, start.get_dist_from_start())
    vis = set()
    while q:
        curr = q.pop()
        if not curr.is_valid():
            continue
        if curr in vis:
            continue
        vis.add(curr)
        if curr.is_finished():
            return curr
        for nbor in curr.get_neighbors():
            q.push(nbor, nbor.get_dist_from_start() + nbor.get_dist_to_finish_heuristic())
    return None


def main():
    level_detail = [
        [green, pink, red, purple],
        [green, orange, red, lime],
        [orange, green, brown, gray],
        [pink, yellow, purple, pink],
        [gray, orange, blue, lime],
        [blue, lime, yellow, sky],
        [sky, blue, aqua, brown],
        [sky, red, blue, gray],
        [brown, orange, aqua, purple],
        [lime, aqua, sky, pink],
        [green, yellow, yellow, gray],
        [purple, aqua, red, brown]
    ]
    layout = Layout.from_level_detail(level_detail)
    print('Layout:')
    print(layout)
    print()

    start = SearchState(layout, None, None, 0)
    end = search(start, True)
    if not end:
        print('No solution')
        return
    cur = end
    moves = []
    while cur.parent:
        moves.insert(0, cur.move)
        cur = cur.parent
    print(f'Solution in {len(moves)} moves:')
    print('\n'.join(f'{i:>3}. {e}' for i, e in enumerate(moves, 1)))


if __name__ == '__main__':
    main()
