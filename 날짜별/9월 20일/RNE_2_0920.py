import time 
import random


#####################################################################################


# algorithm_2Multi-resolution_advanced
def algorithm_2Multi_Resolution_advanced(points,n,m): #이름바꾸기
    grid = [[0] * (m + 1) for _ in range(m + 1)]
    initialize_grid_advanced(grid,(0, 0), (m, m),0)
    start = time.time()
    fill_grid_advanced(grid, [(1, 1), (m, m)], points)
    end = time.time()
    return grid,end-start


def closest_point_advanced(coord, points):
    """주어진 좌표에 가장 가까운 포인트를 찾습니다."""
    closest = None
    min_distance = float('inf')

    for i,point in enumerate(points):
        if i==0:
            continue
        distance = (point[0] - coord[0]) ** 2 + (point[1] - coord[1]) ** 2
        if distance < min_distance:
            min_distance = distance
            closest = i

    return closest


def fill_grid_advanced(grid, grid_info, points):
    top_left, bottom_right = grid_info

    # 현재 격자의 크기가 3x3이하인 경우
    if (bottom_right[0] - top_left[0] <= 2) and (bottom_right[1] - top_left[1] <= 2):
        for i in range(top_left[0],bottom_right[0]+1):
            for j in range(top_left[1],bottom_right[1]+1):
                if grid[j][i]!=0: # 이미 색칠된 경우
                    continue
                grid[j][i]=closest_point_advanced([i,j],points)
        return

    # 꼭짓점 채우기
    if grid[top_left[1]][top_left[0]]==0: # 왼쪽위
        grid[top_left[1]][top_left[0]]=closest_point_advanced(top_left, points)
    if grid[top_left[1]][bottom_right[0]]==0: # 오른쪽위
        grid[top_left[1]][bottom_right[0]]=closest_point_advanced([bottom_right[0],top_left[1]], points)
    if grid[bottom_right[1]][top_left[0]]==0: # 왼쪽아래
        grid[bottom_right[1]][top_left[0]]=closest_point_advanced([top_left[0],bottom_right[1]], points)
    if grid[bottom_right[1]][bottom_right[0]]==0: # 오른쪽아래
        grid[bottom_right[1]][bottom_right[0]]=closest_point_advanced(bottom_right, points)

    # 꼭짓점 색깔이 모두 같으면 모두 색칠
    a = grid[top_left[1]][top_left[0]];b=grid[top_left[1]][bottom_right[0]];c=grid[bottom_right[1]][top_left[0]];d=grid[bottom_right[1]][bottom_right[0]]
    if (a==b) and (b==c) and (c==d):
        initialize_grid_advanced(grid,top_left,bottom_right,a)



    # 격자를 나누는 기준(중점)
    mid_x = top_left[0] + (bottom_right[0] - top_left[0]) // 2
    mid_y = top_left[1] + (bottom_right[1] - top_left[1]) // 2

    # Top left sub-grid
    fill_grid_advanced(grid, [top_left, (mid_x, mid_y)], points)
    # Top right sub-grid
    fill_grid_advanced(grid, [(mid_x, top_left[1]), (bottom_right[0], mid_y)], points)
    # Bottom left sub-grid
    fill_grid_advanced(grid, [(top_left[0], mid_y), (mid_x, bottom_right[1])], points)
    # Bottom right sub-grid
    fill_grid_advanced(grid, [(mid_x, mid_y), bottom_right], points)


def initialize_grid_advanced(grid, top_left, bottom_right,color):
    """격자의 크기에 따라 2차원 배열을 초기화합니다."""
    width = bottom_right[0] - top_left[0] + 1
    height = bottom_right[1] - top_left[1] + 1
    for i in range(top_left[0], bottom_right[0] + 1):
        for j in range(top_left[1], bottom_right[1] + 1):
            grid[j][i]=color
    return


#####################################################################################


# algorithm_2Multi-resolution
def algorithm_2Multi_Resolution(points,n,m): #이름바꾸기
    ans = [[0] * (m + 1) for _ in range(m + 1)]
    grid = initialize_grid((0, 0), (m, m))
    start = time.time()
    fill_grid(grid, [(1, 1), (m, m)], points)
    end = time.time()
    return grid,end-start



def closest_point(coord, points):
    """주어진 좌표에 가장 가까운 포인트를 찾습니다."""
    closest = None
    min_distance = float('inf')

    for i,point in enumerate(points):
        if i==0:
            continue
        distance = (point[0] - coord[0]) ** 2 + (point[1] - coord[1]) ** 2
        if distance < min_distance:
            min_distance = distance
            closest = i

    return closest


def initialize_grid(top_left, bottom_right):
    """격자의 크기에 따라 2차원 배열을 초기화합니다."""
    width = bottom_right[0] - top_left[0] + 1
    height = bottom_right[1] - top_left[1] + 1
    return [[0 for _ in range(top_left[0], bottom_right[0] + 1)] for _ in range(top_left[1], bottom_right[1] + 1)]

def fill_grid(grid, grid_info, points):
    top_left, bottom_right = grid_info

    # 가장 가까운 포인트를 찾습니다.
    top_left_closest = closest_point(top_left, points)
    top_right_closest = closest_point([bottom_right[0],top_left[1]], points)
    bottom_left_closest = closest_point([top_left[0],bottom_right[1]], points)
    bottom_right_closest = closest_point(bottom_right, points)

    # 현재 격자의 크기가 2x2인 경우
    if (bottom_right[0] - top_left[0] <= 1) and (bottom_right[1] - top_left[1] <= 1):
        grid[top_left[1]][top_left[0]]=top_left_closest
        grid[top_left[1]][bottom_right[0]]=top_right_closest
        grid[bottom_right[1]][top_left[0]]=bottom_left_closest
        grid[bottom_right[1]][bottom_right[0]]=bottom_right_closest
        return


    # 모든 꼭지점이 동일한 포인트를 가리키는 경우
    if (top_left_closest == top_right_closest) and (top_right_closest == bottom_left_closest) and (bottom_left_closest == bottom_right_closest):
        for i in range(top_left[1], bottom_right[1]+1):
            for j in range(top_left[0], bottom_right[0]+1):
                grid[i][j] = top_left_closest
        return

    mid_x = top_left[0] + (bottom_right[0] - top_left[0]) // 2
    mid_y = top_left[1] + (bottom_right[1] - top_left[1]) // 2

    # Top left sub-grid
    fill_grid(grid, [top_left, (mid_x, mid_y)], points)
    # Top right sub-grid
    fill_grid(grid, [(mid_x+1, top_left[1]), (bottom_right[0], mid_y)], points)
    # Bottom left sub-grid
    fill_grid(grid, [(top_left[0], mid_y+1), (mid_x, bottom_right[1])], points)
    # Bottom right sub-grid
    fill_grid(grid, [(mid_x+1, mid_y+1), bottom_right], points)


#####################################################################################


# 테스트 코드

def algorithm_2basic(points,n,m):
    ans = [[0] * (m + 1) for _ in range(m + 1)]
    start = time.time()
    for i in range(1, m + 1):
        for j in range(1, m + 1):
            val = 1e9
            idx = 0
            for k in range(1, n + 1):
                distant=(i - points[k][0]) * (i - points[k][0]) + (j - points[k][1]) * (j -points[k][1] )
                if val > distant:
                    val = distant
                    idx = k
            ans[j][i] = idx
    end = time.time()
    return ans,end-start

def test(n,m):
    points = [[0] * 2 for _ in range(n + 1)]

    for i in range(1, n + 1):
        points[i][0], points[i][1] = random.random()*m,random.random()*m

    ans,time=algorithm_2basic(points,n,m)
    new_ans,new_time=algorithm_2Multi_Resolution(points,n,m) #이름바꾸기
    n_ans,n_time=algorithm_2Multi_Resolution_advanced(points,n,m)

    is_not_same=False
    for i in range(1, m + 1):
        for j in range(1, m + 1):
            if new_ans[i][j]!=ans[i][j] or n_ans[i][j]!=ans[i][j]:
                print(i,j,new_ans[i][j],n_ans[i][j],ans[i][j])
                is_not_same=True

    if is_not_same:
        print('윤하')
        return


    print(f'n:{n}, m:{m}')
    print()

    print('basic 걸린 시간 :')
    print(f'\t\t\t\t\t{time:.6f}초')
    print('2Multi_Resolution 걸린 시간 :') #이름바꾸기
    print(f'\t\t\t\t\t{new_time:.6f}초')
    print('2Multi_Resolution_advanced 걸린 시간 :') #이름바꾸기
    print(f'\t\t\t\t\t{n_time:.6f}초')
    print()
    print()

random.seed(10)

# nm^2 = 5000000
test(782,80)
test(500,100)
test(125,200)
test( 20,500)