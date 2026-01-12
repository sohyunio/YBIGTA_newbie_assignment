from __future__ import annotations
from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional, Callable, cast


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
        if isinstance(value, int) and isinstance(self.tree[pos], int):
            self.tree[pos] = cast(U, self.tree[pos] + value) # type: ignore
        else:
            self.tree[pos] = value

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
        res: U = self.identity
        l = left - 1 + self.size
        r = right - 1 + self.size

        while l < r:
            if l % 2 == 1:
                res = self.merge(res, self.tree[l])
                l += 1
            if r % 2 == 1:
                r -= 1
                res = self.merge(res, self.tree[r])
            l //= 2
            r //= 2
        return res
    
    def find_kth(self, k: int) -> int:
        """
        누적합 기준 k번째 원소의 인덱스 찾기
        """
        if cast(int, self.tree[1]) < k: # type: ignore
            return self.size - 1
        
        pos = 1
        while pos < self.size:
            left_val = cast(int, self.tree[pos * 2]) # type: ignore
            if left_val >= k:
                pos = pos * 2
            else:
                k -= left_val
                pos = pos * 2 + 1
        return pos - self.size

