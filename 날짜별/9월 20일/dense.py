n,m = map(int, input().split())
points = [[0] * 3 for _ in range(n)]

for i in range(0, n):
	points[i][0], points[i][1] = map(float, input().split())
	points[i][0] -= 1
	points[i][1] -= 1
	points[i][2] = i

def solve(points,n,m,k=1):
  ans = [[0] * (m) for _ in range(m)]
  points.sort(key=lambda point: (point[0], point[1]))

  def gauss_down(x):
    return int(x)
  def gauss_up(x):
    if int(x) == x:
      return int(x)
    else: return int(x+1)

  def transformation(x):
    if x>=m-1:
      return m-1
    elif x<=0:
      return 0
    else:
      return x

  def binary_search(array,start,end,x,y):
    while start*k<end*k:
      mid = (start+end) // 2
      if array[transformation(x+mid)][transformation(y+mid)] - array[transformation(x+mid)][transformation(y-mid-1)] - array[transformation(x-mid-1)][transformation(y+mid)] + array[transformation(x-mid-1)][transformation(y-mid-1)] == 0:
        start = mid + k
      else:
        end = mid
    return start

  include_list = [[0] * (m) for _ in range(m)]
  include_dictionary = {}
  for i in range(m):
    for j in range(m):
      include_dictionary[(i,j)]=[]
  for idx,point in enumerate(points):
    include_list[gauss_up(point[0])][gauss_up(point[1])] += 1
    include_dictionary[(gauss_up(point[0]),gauss_up(point[1]))].append(idx)

  prefix_sum = [[0] * (m+1) for _ in range(m+1)]
  for i in range(1,m+1):
    for j in range(1,m+1):
      prefix_sum[i][j] = prefix_sum[i-1][j] + prefix_sum[i][j-1] - prefix_sum[i-1][j-1] + include_list[i-1][j-1]

  new_prefix_sum = []
  for i in range(1,m+1):
    new_prefix_sum.append(prefix_sum[i][1:])

  for x in range(m):
    for y in range(m):
      d = binary_search(new_prefix_sum,1,m-1,x,y)
      d = gauss_up((2**0.5)*d+1)
      point_list = []

      for z in range(transformation(x-d),transformation(x+d)+1):
        for w in range(transformation(y-d),transformation(y+d)+1):
          if include_list[z][w] > 0:
            for i in include_dictionary[(z,w)]:
              point_list.append(i)
      val = 1e9
      idx = 0
      for t in range(len(point_list)):
          if val > (x-points[point_list[t]][0])*(x-points[point_list[t]][0])+(y-points[point_list[t]][1])*(y-points[point_list[t]][1]):
              val = (x-points[point_list[t]][0])*(x-points[point_list[t]][0])+(y-points[point_list[t]][1])*(y-points[point_list[t]][1])
              idx = t
      ans[x][y] = points[point_list[idx]][2]
  for i in range(m):
    for j in range(m):
      print(ans[i][j], end=' ')
    print()

solve(points, n, m)