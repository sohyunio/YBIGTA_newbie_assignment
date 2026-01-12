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




import sys

input = sys.stdin.readline


"""
TODO:
- 일단 SegmentTree부터 구현하기
- main 구현하기
"""


def main() -> None:
    # 구현하세요!
    '''
    segment tree 이용 사탕 상자 관리
    
    - 맛 번호를 인덱스로 하여 사탕 개수 저장
    - 누적합 기준 k번째 원소의 인덱스 찾기
    - 사탕 추가 및 제거 연산 처리
    '''
    n = int(input())
    MAX = 1000000
    
    seg: SegmentTree[int, int] = SegmentTree(
    MAX,
    merge=lambda a, b: a + b,
    identity=0
    )

    
    for _ in range(n):
        cmd = list(map(int, input().split()))
        
        if cmd[0] == 1:
            # 1 B: B번째 사탕 꺼내기
            B = cmd[1]
            # 2. find_kth는 0-based index를 반환하므로 +1을 해서 맛 번호 복원
            taste_idx = seg.find_kth(B)
            actual_taste = taste_idx + 1
            
            print(actual_taste)
            # 꺼낸 사탕 하나 제거
            seg.update(actual_taste, -1)

        else:
            # 2 B C: 맛 B 사탕 C개 추가
            _, B, C = cmd
            seg.update(B, C)

if __name__ == "__main__":
    main()