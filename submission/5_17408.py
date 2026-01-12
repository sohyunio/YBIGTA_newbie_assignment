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
    



import sys
input = sys.stdin.readline

INF = 10**18

"""
TODO:
- 일단 SegmentTree부터 구현하기
- main 구현하기
"""


class Pair(tuple[int, int]):
    """
    힌트: 2243, 3653에서 int에 대한 세그먼트 트리를 만들었다면 여기서는 Pair에 대한 세그먼트 트리를 만들 수 있을지도...?
    """
    def __new__(cls, a: int, b: int) -> 'Pair':
        return super().__new__(cls, (a, b))

    @staticmethod
    def default() -> 'Pair':
        """
        기본값
        이게 왜 필요할까...?
        """
        return Pair(0, 0)

    @staticmethod
    def f_conv(w: int) -> 'Pair':
        """
        원본 수열의 값을 대응되는 Pair 값으로 변환하는 연산
        이게 왜 필요할까...?
        """
        return Pair(w, 0)

    @staticmethod
    def f_merge(a: Pair, b: Pair) -> 'Pair':
        """
        두 Pair를 하나의 Pair로 합치는 연산
        이게 왜 필요할까...?
        """
        return Pair(*sorted([*a, *b], reverse=True)[:2])

    def sum(self) -> int:
        return self[0] + self[1]


def main() -> None:
    '''
    입력 받아 segment tree 생성 후,
    두 종류의 쿼리 처리
    1 i v: A[i] = v
    2 l r: A[l..r] 구간에서 가장 큰 두 수의 합
    '''
    # 구현하세요!
    N = int(input())
    A = list(map(int, input().split()))
    Q = int(input())

    seg = SegmentTree(A,
        Pair.default,
        Pair.f_conv,
        Pair.f_merge
        )

    for _ in range(Q):
        q = list(map(int, input().split()))
        if q[0] == 1:
            _, i, v = q
            seg.update(i - 1, v)
        else:
            _, l, r = q
            res = seg.query(l - 1, r - 1)
            print(res.sum())
    pass


if __name__ == "__main__":
    main()