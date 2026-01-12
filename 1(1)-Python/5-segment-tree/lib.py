from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional, Callable


"""
TODO:
- SegmentTree 구현하기
"""


T = TypeVar("T")
U = TypeVar("U")


class SegmentTree(Generic[T, U]):
    # 구현하세요!
    def __init__(self, n: int, merge: Callable[[U, U], U], identity: U):
        '''
        n   : 관리 원소 개수
        merge   : 두 구간 합치기
        identity    : 항등원
        '''
        self.merge = merge
        self.identity = identity
        
        self.size = 1
        while self.size < n:
            self.size *= 2
        
        self.tree = [identity] * (self.size * 2)

    def update(self, idx: int, value: U) -> None:
        '''
        idx 위치의 값을 value만큼 증가/감소
        '''
        pos = idx - 1 + self.size
        self.tree[pos] += value

        pos //= 2
        while pos > 0:
            self.tree[pos] = self.merge(
                self.tree[pos * 2],
                self.tree[pos * 2 + 1]
            )
            pos //= 2
    pass

    def query(self, left: int, right: int) -> U:
        '''
        [left, right) 구간 합
        '''
        res = self.identity
        left += self.size
        right += self.size

        while left < right:
            if left % 2 == 1:
                res = self.merge(res, self.tree[left])
                left += 1
            if right % 2 == 1:
                right -= 1
                res = self.merge(res, self.tree[right])

            left //= 2
            right //= 2

        return res
    
