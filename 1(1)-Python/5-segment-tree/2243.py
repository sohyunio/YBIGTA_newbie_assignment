from lib import SegmentTree
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