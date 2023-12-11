import time
import random 

n,m = 10,10
points = [[0] * 2 for _ in range(n)]

for i in range(0, n):
	points[i][0], points[i][1] = random.random()*(m-1),random.random()*(m-1)

def algorithm3_around(points,n,m,k=1):
  # 점 및 격자 배열 세팅
  ans = [[0] * (m) for _ in range(m)]
  points.sort(key=lambda point: (point[0], point[1]))

  # 정수화 함수
  def gauss_down(x):
    return int(x)
  def gauss_up(x):
    if int(x) == x:
      return x
    else: return int(x+1)

  # 배열에 넣기 위한 크기 조절 함수
  def transformation(x):
    if x>=m-1:
      return m-1
    elif x<=0:
      return 0
    else:
      return x

  # 이분 탐색으로 점이 존재하는 최소의 범위 구하기
  def binary_search(array,start,end,x,y):
    while start*k<end*k:
      mid = (start+end) // 2
      if array[transformation(x+mid)][transformation(y+mid)] - array[transformation(x+mid)][transformation(y-mid-1)] - array[transformation(x-mid-1)][transformation(y+mid)] + array[transformation(x-mid-1)][transformation(y-mid-1)] == 0:
        start = mid + k
      else:
        end = mid
    return start

  start = time.time()
  # 누적합 배열 만들기
  include_list = [[0] * (m) for _ in range(m)] # 점이 격자 내에 존재하는지 여부 판단
  include_dictionary = {} # 점이 존재하는 위치를 key, 그 점의 인덱스를 value로 하는 딕셔너리
  for i in range(m):
    for j in range(m):
      include_dictionary[(i,j)]=[]
  for idx,point in enumerate(points): # 이 이후로는 points 섞으면 안됨
    include_list[gauss_up(point[0])][gauss_up(point[1])] += 1 # 점이 있으면 + 1
    include_dictionary[(gauss_up(point[0]),gauss_up(point[1]))].append(idx) # 튜플 형태로 격자점 좌표를 key로 넣어줌

  prefix_sum = [[0] * (m+1) for _ in range(m+1)] # 누적합 배열
  for i in range(1,m+1):
    for j in range(1,m+1):
      prefix_sum[i][j] = prefix_sum[i-1][j] + prefix_sum[i][j-1] - prefix_sum[i-1][j-1] + include_list[i-1][j-1]

  new_prefix_sum = []
  for i in range(1,m+1):
    new_prefix_sum.append(prefix_sum[i][1:])
  # print(new_prefix_sum)

  # for x in range(m):
  #   for y in range(m):
  #     print(new_prefix_sum[x][y],end=' ')
  #   print()

  # print(binary_search(new_prefix_sum,1,m-1,0,2))

  # for x in range(m):
  #   for y in range(m):
  #     print(include_list[x][y],end=' ')
  #   print()

  # 각 격자점마다 주위 범위에 대해서 가장 가까운 점 찾기 (점과 격자점 구별하기)
  for x in range(m):
    for y in range(m):
      d = binary_search(new_prefix_sum,1,m-1,x,y)
      d = gauss_up((2**0.5)*d+1) # 실제 조사할 범위
      point_list = [] # 범위 안에 있는 점들 저장할 리스트

      for z in range(transformation(x-d),transformation(x+d)+1):
        for w in range(transformation(y-d),transformation(y+d)+1):
          if include_list[z][w] > 0: # 점이 있으면 include_list[z][w] == 1 -> (z-1,w-1)~(z,w)에 점이 있다는 뜻
            for i in include_dictionary[(z,w)]:
              point_list.append(i) # 점의 인덱스를 추가 
            # if (z, w) in include_dictionary.keys: pass
            # else:
      val = 1e9
      idx = 0
      for t in range(len(point_list)):
          if val > (x-points[point_list[t]][0])*(x-points[point_list[t]][0])+(y-points[point_list[t]][1])*(y-points[point_list[t]][1]):
              val = (x-points[point_list[t]][0])*(x-points[point_list[t]][0])+(y-points[point_list[t]][1])*(y-points[point_list[t]][1])
              idx = t
      ans[x][y] = point_list[idx]
  end = time.time()
  # ans 확인
  # for x in range(m):
  #   for y in range(m):
  #     print(ans[x][y],end=' ')
  #   print()
  return ans,(end-start)