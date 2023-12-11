class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Line:
    def __init__(self,pt1,pt2,x1,x2): # pt1, pt2는 수직이등분선의 주인 , x1,x2는 경계의 x좌표 (x1<x2)
        self.owner = [pt1,pt2]
        self.x1 = int(x1+1)
        self.x2 = int(x2)
    
    def function_value(self,x):
        return -(self.owner[1].x-self.owner[0].x)/(self.owner[1].y-self.owner[0].y)*(x-self.owner[0].x) + self.owenr[0].y

def distance(x1,y1,x2,y2):
    return ((x1-x2)**2+(y1-y2)**2)**0.5

m = int(input()) 

line_list = [] # Line 객체가 저장될 리스트 
point_list = [] # 처음 주어지는 n개 점 리스트 

li = [[0 for _ in range(m+2)] for _ in range(m+2)] 

# 직선에 인접한 위 아래 점을 -1로 바꿈 
for line in line_list:
    for i in range(max(1,line.x1),min(line.x2,m)+1): 
        y = line.function_value(i)
        if 0 < y < m+1: # 격자점 범위를 넘어가는 것을 막기 위한 부등식 
            li[i][int(y)] = -1 
            li[i][int(y)+1] = -1 

start_point = {} # 처음 주어진 n개 점과 가장 가까운 격자점을 저장하는 딕셔너리 

# 처음 주어진 n개 점과 가장 가까운 격자점에는 1을 부여 
for point in point_list:
    x = round(point.x)
    y = round(point.y)
    li[x][y] = 1 
    start_point[Point(x,y)] = point 

dic = {} # key : node, value  : 인접 node  

# 각 노드 (격자점)의 인접노드를 dic에 추가 
for i in range(0,m+2):
    for j in range(0,m+2):
        dic[Point(i,j)] = [] 

for i in range(1,m+1):
    for j in range(1,m+1):
        if li[i][j] != -1:
            dic[Point(i,j)] = [Point(i-1,j),Point(i+1,j),Point(i,j-1),Point(i,j+1)] 
    
    
def bfs(graph, start): # Dict 자료형 형태로 준다. key는 노드, value는 인접노드를 가리킨다.
    visited = {i:False for i in graph.keys()} # 방문 배열. visited[node] = True이면 node는 방문이 끝난 상태이다.
    queue = [start]
    visited[start] = True
    while len(queue) > 0: # 큐가 빌 때까지 반복
        current = queue.pop(0) #queue에서 노드를 하나 빼 온다. 이 노드를 current라고 하자.
        for nxt in graph[current]: # current의 인접 노드들을 확인한다. 이 각각의 노드를 nxt라고 하자.
            if not visited[nxt]: # 만일 nxt에 방문하지 않았다면
                #nxt 방문
                queue.append(nxt)
                visited[nxt] = True
    return visited

voronoi_diagram = {}

for startpoint in list(start_point.keys()):
    cell = []
    visited = bfs(dic,startpoint) 
    for key,value in visited.items(): # key의 형식 : Point 객체 
        if value: # value값이 True인 key들만 cell에 추가 
            if 1 <= key.x <= m and 1 <= key.y <= m:
                cell.append(key) 
    voronoi_diagram[start_point[startpoint]] = cell 

''''
bfs 코드 설명 

1. Point와 Line 클래스를 만듦 -> Line 클래스는 직선의 주인인 두 점과 경계점의 x좌표를 property로 가짐 , 또한 function_value 함수로 두 주인인 점의 수직이등분선의 함숫값을 반환 
2. 각 직선의 위 아래 점은 -1을 부여 , 주어진 n개의 점 각각과 가장 가까운 격자점들에는 1을 부여 
3. m+2 * m+2 배열을 만들어서 bfs를 위한 딕셔너리를 만듦 
4. bfs에서는 m+2*m+2 개의 격자점을 key로 하고 value가 True / False인 딕셔너리를 반환 
   startpoint를 시작 노드로 하여 반환된 딕셔너리에서 True 값을 가지는 key(격자점)들은 startpoint에 대응되는 point의 셀에 포함됨

   또한 -1 값이 부여된 격자점에는 인접 노드를 부여하지 않음으로써 노드를 확장하다가 -1을 만나게 되면 bfs가 종료됨 -> 정확히 셀에 해당되는 부분만 True 값을 가지게 할 수 있음  
'''

  
