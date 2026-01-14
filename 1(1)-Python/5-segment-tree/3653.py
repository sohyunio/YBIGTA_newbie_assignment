from lib import SegmentTree
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

        seg: SegmentTree[int, int] = SegmentTree(
            n+m+1,
            merge=lambda a, b: a + b,
            identity=0
        )

        pos = [0] * (n + 1)

        # 초기 배치
        for dvd in range(1, n + 1):
            position = m + dvd
            pos[dvd] = position
            seg.update(position, 1)

        top = m
        commands = list(map(int, input().split()))

        results = []

        for dvd in commands:
            cur_pos = pos[dvd]

            # 위에 있는 DVD 개수
            above = seg.query(1, cur_pos)
            results.append(str(above))

            # 제거
            seg.update(cur_pos, -1)

            # 맨 위로 이동
            pos[dvd] = top
            seg.update(top, 1)
            top -= 1
        print(" ".join(results))
    pass


if __name__ == "__main__":
    main()