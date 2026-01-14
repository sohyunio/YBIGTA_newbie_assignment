from __future__ import annotations
import copy
from collections import deque
from collections import defaultdict
from typing import DefaultDict, List


"""
TODO:
- __init__ 구현하기
- add_edge 구현하기
- dfs 구현하기 (재귀 또는 스택 방식 선택)
- bfs 구현하기
"""


class Graph:
    def __init__(self, n: int) -> None:
        """
        그래프 초기화
        n: 정점의 개수 (1번부터 n번까지)
        """
        self.n = n
        # 구현하세요!
        self.graph = [[0]*(n+1) for _ in range(n+1)]

    
    def add_edge(self, u: int, v: int) -> None:
        """
        양방향 간선 추가
        """
        # 구현하세요!
        self.graph[u][v] = 1
        self.graph[v][u] = 1
        pass
    
    def dfs(self, start: int) -> list[int]:
        """
        깊이 우선 탐색 (DFS)
        
        구현 방법: 재귀 방식
        1. 재귀 방식: 함수 내부에서 재귀 함수 정의하여 구현
        2. 스택 방식: 명시적 스택을 사용하여 반복문으로 구현

        시작 정점에서 DFS 탐색 후 방문 순서 리스트 반환
        """
        # 구현하세요!
        visited = [0] * (self.n+1)
        result: list[int] = []
        visited[start] = 1
        def _dfs(v):
            visited[v] = 1
            result.append(v)
            for i in range(1, self.n + 1):
                if not visited[i] and self.graph[v][i]:
                    _dfs(i)

        _dfs(start)
        return result
        pass
    
    def bfs(self, start: int) -> list[int]:
        """
        너비 우선 탐색 (BFS)
        큐를 사용하여 구현

        시작정점에서 BFS 탐색 후 방문 순서 리스트 반환
        """
        # 구현하세요!
        visited = [0] * (self.n+1)
        result: list[int] = []

        visited[start] = 1
        q = deque([start])

        while q:
            v = q.popleft()
            result.append(v)
            for i in range(1, self.n+1):
                if not visited[i] and self.graph[v][i]:
                    q.append(i)
                    visited[i] = 1
        return result
        pass
    
    def search_and_print(self, start: int) -> None:
        """
        DFS와 BFS 결과를 출력
        """
        dfs_result = self.dfs(start)
        bfs_result = self.bfs(start)
        
        print(' '.join(map(str, dfs_result)))
        print(' '.join(map(str, bfs_result)))
