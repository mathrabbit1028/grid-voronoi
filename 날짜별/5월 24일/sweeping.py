#sweeping
import math

lines=[]

#보로노이 다이어그램에서의 간선을 나타내는 클래스
class line:
    def __init__(self,position,owner) -> None:
        #position[0]=(x1,y1) position[1]=(x2,y2)
        self.x1=position[0][0]
        self.y1=position[0][1]
        self.x2=position[1][0]
        self.y2=position[1][1]
        self.color=[owner[0],owner[1]]
        # 보로노이 다이어그램에서의 간선은 항상 두 점의 수직이등분선이 되고
        # 이 수직이등분선은 그 두 점이 차지하는 영역을 나누기 때문에 이 간선과   
        # 인접한 영역은 color가 그 두 점이 된다.
    
    def equation(self,x):
        # 이 함수는 직선의 방정식 y = mx + b 에서 m, b 값을 사용하여 y 값을 계산합니다.
        return float(self.y2-self.y1)/(self.x2-self.x1)*(x-self.x1)+self.y1

n=10
m=100
def range_manipulation(x):
    # 범위를 조정하는 함수입니다. 주어진 x 값이 0과 m-1 사이에 있는지 확인하고, 그렇지 않으면 경계값으로 조정합니다.
    if x<0: x=0
    elif x>m-1: x=m-1
    return x

# 각 점에 대한 라인 정보를 저장하는 3차원 배열을 만듭니다.
segment=[[[] for _ in range(n)] for _ in range(m)]

# 각 격자를 이루는 선분에 대해, 라인이 통과하는 x 좌표에 대해 해당하는 y 좌표를 계산하고 저장합니다.
for item in lines:
    left=range_manipulation(math.floor(item.x1+1))
    right=range_manipulation(math.floor(item.x2))
    for x in range(left,right+1):
        segment[x][item.color[0]].append(range_manipulation(item.equation(x)))
        segment[x][item.color[1]].append(range_manipulation(item.equation(x)))


# 최종 보드를 생성합니다. 각 격자점에는 가장 가까이에 있는 점의 인덱스가 저장됩니다.
board=[[0 for _ in range(m)] for _ in range(m)]

for x in range(m):
    for i in range(n):
        if len(segment[x][i])==2:
            segment[x][i].sort()
            # 영역에 저장된 구간를 활용하여 구간 내의 격자점에 인덱스를 저장한다.
            for y in range(math.floor(segment[x][i][0]+1),math.floor(segment[x][i][1])+1):
                board[x][y]=i

print(board)