from lib import SegmentTree
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
        return super().__new__(cls, [a, b])  # type: ignore

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

    seg: SegmentTree[Pair, Pair] = SegmentTree(
        n=N,
        merge=Pair.f_merge,
        identity=Pair.default()
    )

    # 초기 배열 A를 세그먼트 트리에 반영
    for i, v in enumerate(A):
        seg.update(i + 1, Pair.f_conv(v))

    for _ in range(Q):
        q = list(map(int, input().split()))
        if q[0] == 1:
            _, i, v = q
            seg.update(i, Pair.f_conv(v))
        else:
            _, l, r = q
            res = seg.query(l, r)
            print(res.sum())
    pass


if __name__ == "__main__":
    main()