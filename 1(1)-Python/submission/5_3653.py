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


"""
TODO:
- 일단 SegmentTree부터 구현하기
- main 구현하기
"""


def main() -> None:
    '''
    segment tree로 DVD 관리 문제 해결

    - 각 DVD의 위치를 인덱스로 관리
    - 누적합으로 현재 DVD 위에 있는 개수 계산
    - 꺼낸 DVD 항상 맨 위로 이동
    '''
    # 구현하세요!
    T = int(input())
    for _ in range(T):
        n, m = map(int, input().split())

        seg = SegmentTree(n + m)

        pos = [0] * (n + 1)

        # 초기 배치
        for dvd in range(1, n + 1):
            position = m + dvd - 1
            pos[dvd] = position
            seg.update(position, 1)

        top = m - 1
        commands = list(map(int, input().split()))

        for dvd in commands:
            cur_pos = pos[dvd]

            # 위에 있는 DVD 개수
            above = seg.query(0, cur_pos)
            print(above, end=" ")

            # 제거
            seg.update(cur_pos, -1)

            # 맨 위로 이동
            pos[dvd] = top
            seg.update(top, 1)
            top -= 1
    pass


if __name__ == "__main__":
    main()