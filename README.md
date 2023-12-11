# grid-voronoi (Research)

## Introduction

2023 SSHS RnE (이동원, 이민섭, ~~이채운~~, 정민건)

- 코드 테스트를 위한 polygon package
- 각 일차별 산출물
- 최종 논문(hwp), 최종 논문(Tex), 발표자료 ppt

## Problem
$N$개의 _seed_ 의 위치가 주어질 때 각 $M^2$개의 격자점 $(i, j) (1 \leq i \leq M, 1 \leq j \leq M)$과 가장 가까운 _seed_ 의 번호 최솟값 출력하기

## Algorithms

- _Dijkstra_ : $O(T^2 * M^2 \log M)$, 격자를 그래프로 만든 후 다익스트라 알고리즘의 원리 활용
- _Sparse_ : ?, 각 사분면으로 분할 후 네 꼭짓점과 가장 가까운 _seed_ 가 동일하면 안을 모두 채우고, 아니면 게속 분할
- _Dense_ : $O(M^4/N + M^2 \log M)$, 각 점에 대해 점이 존재하는 주변 정사각형을 이분탐색으로 찾고, 그 안만 탐색
- _Merge_ : $O(M^2 \log^2 M)$, _Dense_ 에서 탐색할 점을 쿼드 트리로 관리하여 더 빠르게 점의 목록을 구하기
- _BFS_ : $O(M^2 + NM + N \log N)$, 보르노이 다이어그램을 구하는 코드로 경계를 구하고 경계에서부터 BFS
- _Sweeping_ : $O(M^2 + NM + N \log N)$, 보르노이 다이어그램을 구하는 코드로 경계를 구하고 경계를 넘어가기 전까지는 가장 가까운 _seed_ 가 동일함을 이용해 채우기

## Performance

정점 개수 $N=3 \times 10^5$, 격자 크기 $M = 4 \times 10^3$에서 _Sweeping_ 이 약 7.5초에 답을 구함. 에상된 나이브 알고리즘 $O(NM^2)$의 수행 시간 7784초보다 1000배 이상 개선됨
