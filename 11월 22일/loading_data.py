# 경로 변수 저장
csv_path = "plot_by_n_fig.csv"

# 상수 정의하기
min_value = 1
max_value = 200000
type_of_graph = 'n'
fixed_value = 1000
time_upper = 15000

#부가적인 전처리
type_of_fixed_value= 'm' if type_of_graph == 'n' else 'n'

import numpy as np
import pandas as pd
from tqdm import tqdm

# 엑셀 파일 읽기
print('엑셀 파일 읽는중\n')
df = pd.read_csv(csv_path, usecols=[0,1, 2, 3])
print(df.info())
print(df.head(5))
print(df['name'].value_counts().index)
df['time'].replace('TLE',np.nan,inplace=True)
df['time']=df['time'].astype(float)
print(df.info())

'''	n min n max 안에 있는 모든 데이터 불러와서
	n 기준 오름차순 Series 만들기'''
algorithm_list=list(df['name'].value_counts().index)
name_list=[]
df_list=[]
print('\n기본 데이터프레임 처리')
for name in tqdm(algorithm_list):
	df_tmp=df[(df['name']==name)&(df[type_of_fixed_value]==fixed_value)&(df[type_of_graph]>=min_value)&(df[type_of_graph]<=max_value)&(df['time']<time_upper)]
	df_tmp = pd.DataFrame(df_tmp.groupby(type_of_graph).mean()).reset_index()
    # print(df_tmp.info())
	df_list.append(df_tmp)
	name_list.append(name)


# 각 시리즈에서 최대값과 최소값을 파악하기 위한 초기값 설정
global_min_x = float('inf')
global_max_x = float('-inf')
global_min_y = float('inf')
global_max_y = float('-inf')

# df_list 내의 각 시리즈에 대해서
print('\n최대 최소 찾기')
for df_tm in tqdm(df_list):
    # 로그형 그래프
    # df_tm[type_of_graph]=np.log10(df_tm[type_of_graph])
    # df_tm['time']=np.log10(df_tm['time'])

    # 시리즈의 인덱스(x축 값)의 최소값과 최대값을 파악
    min_x = df_tm[type_of_graph].min()
    max_x = df_tm[type_of_graph].max()
    
    # 시리즈의 값(y축 값)의 최소값과 최대값을 파악
    min_y = df_tm['time'].min()
    max_y = df_tm['time'].max()
    
    # 현재 시리즈의 최소값과 최대값을 기반으로 전체 데이터의 최소값과 최대값 갱신
    global_min_x = min(global_min_x, min_x)
    global_max_x = max(global_max_x, max_x)
    global_min_y = min(global_min_y, min_y)
    global_max_y = max(global_max_y, max_y)

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# 그래프를 그리기 위한 설정
plt.figure(figsize=(10, 6))

print(global_min_x,global_max_x)
print(global_min_y,global_max_y)
plt.xlim(global_min_x, global_max_x)
plt.ylim(global_min_y, global_max_y)

# df_list의 각 Series에 대하여 그래프를 그림
print('\n그래프 그리는중')
for dataframe, name in tqdm(zip(df_list, name_list)):
	# Sort the dataframe based on the 'type_of_graph' column
	dataframe = dataframe.sort_values(by=type_of_graph)
	dataframe.head(10)
	plt.plot(dataframe[type_of_graph], dataframe['time'], label=name)


# 범례 표시
plt.legend()

# 그래프의 제목, x축 및 y축 라벨 설정
plt.title('Computation time of Algorithms')
plt.xlabel('Number of Seed' if type_of_graph == 'n' else 'Size of Grid')
plt.ylabel('Time (ms)')

plt.xscale('log')
plt.yscale('log')

fig = plt.gcf()

# 그래프 출력
plt.show()

if input('그래프를 저장하시겠습니까?(y/n)').lower()=='y':
	file_name = "graph_output.png"  # You can change this to your preferred file name and format (e.g., .jpg, .pdf)
	fig.savefig(file_name, dpi=300)  # dpi is dots per inch, you can adjust this for desired resolution
