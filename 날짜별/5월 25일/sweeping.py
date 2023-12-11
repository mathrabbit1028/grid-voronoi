#sweeping
import math
from scipy.spatial import Delaunay
import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
from matplotlib.markers import MarkerStyle
import random
import sympy as sp

def plot_voronoi(points):
    # Voronoi 다이어그램 계산
    vor = Voronoi(points)

    size=6

    # Voronoi 다이어그램 시각화
    fig=voronoi_plot_2d(vor)
    fig.set_size_inches(size*1.2,size)

    # 입력된 점 플롯
    plt.plot(points[:, 0], points[:, 1], 'ko')

    # 축 범위 설정
    plt.xlim(0, m)
    plt.ylim(0, m)

    # 그래프 출력
    plt.show()

# 임의의 2D 점들 생성
n=20
m=40
points = np.array([[random.random()*m,random.random()*m] for _ in range(n)])
plot_voronoi(points)

#상수
LEFT=1
RIGHT=-1

# 드로네 삼각화 생성
tri = Delaunay(points)

def circumcenter(point1, point2, point3):
    # 세 점의 좌표를 불러옴
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3

    # 세 점의 중점을 계산
    mid_point12 = ((x1 + x2) / 2, (y1 + y2) / 2)
    mid_point23 = ((x2 + x3) / 2, (y2 + y3) / 2)

    # 선분을 수직으로 가로지르는 선의 기울기를 계산
    slope12 = (y2 - y1) / (x2 - x1)
    slope23 = (y3 - y2) / (x3 - x2)

    # 선분을 수직으로 가로지르는 선의 방정식
    #12 : y = -1 / slope12(x - mid_point12[0]) + mid_point12[1]
    #23 : y = -1 / slope23(x - mid_point23[0]) + mid_point23[1]

    # 두 선의 계수와 상수를 계산
    a1,b1=-1/slope12,1/slope12*mid_point12[0]+mid_point12[1]
    a2,b2=-1/slope23,1/slope23*mid_point23[0]+mid_point23[1]

    # 값을 대입
    circumcenter = ((b2-b1)/(a1-a2),a1*(b2-b1)/(a1-a2)+b1)

    return circumcenter


def direction(A, B, C):
    # 세 점의 좌표를 분해
    Ax, Ay = A
    Bx, By = B
    Cx, Cy = C

    # 벡터 AB와 AC를 구함
    AB = [Bx - Ax, By - Ay]
    AC = [Cx - Ax, Cy - Ay]

    # 벡터 AB와 AC의 외적을 구함 (Z축 값만 필요)
    cross_product = AB[0] * AC[1] - AB[1] * AC[0]

    if cross_product > 0:
        return LEFT
    elif cross_product < 0:
        return RIGHT
    else:
        return ValueError

triangles=tri.simplices

lines=dict([])
for triangle in triangles:
    point_indexs=[0,0,0]
    point_coor=[0,0,0]
    for i in range(3):
        point_indexs[i]=triangle[i]
    for j in range(3):
        point_coor[j]=points[point_indexs[j]]
    
    circumcenter_point=circumcenter(point_coor[0],point_coor[1],point_coor[2])

    for i in range(3):
        two_of_point=[int(point_indexs[i-1]),int(point_indexs[i])]
        key=(min(two_of_point),max(two_of_point))
        if key in lines:
            lines[key].append((circumcenter_point))
        else:
            lines[key]=[circumcenter_point]

for triangle in triangles:
    point_indexs=[0,0,0]
    for i in range(3):
        point_indexs[i]=triangle[i]

    for i in range(3):
        two_of_point=[int(point_indexs[i-1]),int(point_indexs[i])]
        key=(min(two_of_point),max(two_of_point))
        if len(lines[key])==1:
            a,b=key
            if points[a][1]>points[b][1]:
                t=a;a=b;b=t
            
            idx=1
            if (points[b][1]-points[a][1])/(points[b][0]-points[a][0])<0:
                idx=-1

            if direction(points[a],points[b],points[point_indexs[i-2]])==RIGHT:
                lines[key].append((-np.inf,idx*np.inf))
            else:
                lines[key].append((np.inf,-idx*np.inf))

input_dic=lines

#보로노이 다이어그램에서의 간선을 나타내는 클래스
class line:
    def __init__(self,position,owner) -> None:
        #position[0]=(x1,y1) position[1]=(x2,y2)
        self.x1=position[0][0]
        self.y1=position[0][1]
        self.x2=position[1][0]
        self.y2=position[1][1]
        self.color=[owner[0],owner[1]]
        self.a=0
        if math.isinf(self.y2) or math.isinf(self.y1):
            self.a=-float(points[self.color[0]][0]-points[self.color[1]][0])/(points[self.color[0]][1]-points[self.color[1]][1])
        else:
            self.a=float(self.y2-self.y1)/(self.x2-self.x1)
        # 보로노이 다이어그램에서의 간선은 항상 두 점의 수직이등분선이 되고
        # 이 수직이등분선은 그 두 점이 차지하는 영역을 나누기 때문에 이 간선과   
        # 인접한 영역은 color가 그 두 점이 된다.
    
    def equation(self,x):
        # 이 함수는 직선의 방정식 y = ax + b 에서 a, b 값을 사용하여 y 값을 계산합니다.
        if math.isinf(self.x2):
            return self.a*(x-self.x1)+self.y1
        if math.isinf(self.x1):
            return self.a*(x-self.x2)+self.y2
        return self.a*(x-self.x2)+self.y2

list_line=[]

for key,item in input_dic.items():
    list_line.append(line((item[0],item[1]),key))

def range_manipulation(x):
    # 범위를 조정하는 함수입니다. 주어진 x 값이 0과 m-1 사이에 있는지 확인하고, 그렇지 않으면 경계값으로 조정합니다.
    if x<0: x=-1
    elif x>m: x=m+1
    return x

# 각 점에 대한 라인 정보를 저장하는 3차원 배열을 만듭니다.
segment=[[[-2,-2] for _ in range(n)] for _ in range(m+1)]

# 각 격자를 이루는 선분에 대해, 라인이 통과하는 x 좌표에 대해 해당하는 y 좌표를 계산하고 저장합니다.
for item in list_line:
    left,right=min(item.x1,item.x2),max(item.x1,item.x2)
    temp=range_manipulation(left)
    temp1=range_manipulation(right)
    left=math.floor(temp)+1
    right=min(math.floor(temp1),m)
    for x in range(left,right+1):
        color_points=[points[item.color[0]],points[item.color[1]]]
        for k in range(2):
            tmp=range_manipulation(item.equation(x))
            if tmp<0 or tmp>m:
                continue
            if color_points[k][1] > item.equation(color_points[k][0]):
                segment[x][item.color[k]][0]=math.floor(tmp)+1
            else:
                segment[x][item.color[k]][1]=math.floor(range_manipulation(item.equation(x)))

# 최종 보드를 생성합니다. 각 격자점에는 가장 가까이에 있는 점의 인덱스가 저장됩니다.
board=[[-2 for _ in range(m+1)] for _ in range(m+1)]

for x in range(m+1):
    for i in range(n):
        low=segment[x][i][0]
        high=segment[x][i][1]
        if low==-2 and high==-2:
            continue
        if low<0:low=0
        if high>m or high<0:high=m
        # 영역에 저장된 구간를 활용하여 구간 내의 격자점에 인덱스를 저장한다.
        for y in range(low,high+1):
            board[y][x]=i

def plot_2d_array(array):
    # 배열의 크기 계산
    rows, cols = array.shape

    # 좌표 생성
    x = np.arange(cols)
    y = np.arange(rows)

    # 좌표 메쉬그리드 생성
    X, Y = np.meshgrid(x, y)

    # 배열 값에 따라 점 색깔 설정
    colors = array.flatten()

    fig=plt.figure()
    width=640/fig.dpi
    height=480/fig.dpi
    fig.set_figwidth(width)
    fig.set_figheight(height)

    # 플롯 그리기
    m=MarkerStyle(marker=",")
    plt.scatter(X.flatten(), Y.flatten(), c=colors,marker=m)
    plt.scatter(points[:,0],points[:,1],c='red')

    # 축 범위 설정
    plt.xlim(0, cols-1)
    plt.ylim(0, rows-1)

    # 컬러바 추가
    plt.colorbar()

    # 그래프 출력
    plt.show()

# 예시 2차원 배열
array = np.array(board)

# 2차원 배열 플롯
plot_2d_array(array)