from a230920_dense import dense_algorithm
from a230920_sparse import algorithm_2Multi_Resolution_advanced
from a230525_basic import algorithm_basic
from a230526_sweeping import sweeping
from a231013_Dijkstra import Dijkstra
import time 
import random  
import pandas as pd 
import multiprocessing

nm_list = [(10,500),(30,500),(100,500),(300,500),(1000,500)]
def_list1 = [dense_algorithm,sweeping] # point list 길이 n인 것 
def_list2 = [algorithm_2Multi_Resolution_advanced,algorithm_basic] # point list 길이 n+1인 것 
recall = 50 # 반복횟수

series_list = []
df = pd.DataFrame([],columns = ['n','m','CPU TIME','def_name'])

if __name__ == '__main__':

    for nm in nm_list:
        n,m = nm[0], nm[1]
        # point list 길이 n인 것  
        for fuc in def_list1:
            sum_time = 0
            points = [[0] * 2 for _ in range(n)]

            for i in range(0, n):
                points[i][0], points[i][1] = random.random()*(m-1),random.random()*(m-1) 

            
            for cnt in range(1,recall+1):
                process = multiprocessing.Process(target=fuc,args=(points,n,m))
                process.start()
                process.join(timeout=150)  # 0.1초 후에 프로세스가 종료되도록 대기

                if process.is_alive():
                    process.terminate()  # 프로세스를 종료
                    result = 'TLE'
                    break
                else:
                    cpu_time = fuc(points,n,m)[1]
                        
                sum_time += cpu_time

            if cnt == recall: # 다 돌았을 때만 시간 저장 
                result = sum_time / recall
            

            series_list.append(pd.Series([n,m,result,str(fuc).split(' ')[1]])) # n,m, 시간, 함수 이름 담은 시리즈 
            print(n,m,result,str(fuc).split(' ')[1]) 

            df = pd.DataFrame(series_list)   
            df.columns = ['n','m','CPU TIME','def_name']

            # index= int(time.time())%10000
            csv_path = f"timedata/time_data_2.csv"
            df.to_csv(csv_path, index=False)

        for fuc in def_list2: 
            sum_time = 0
            points = [[0] * 2 for _ in range(n+1)]

            for i in range(1, n+1):
                points[i][0], points[i][1] = random.random()*(m-1),random.random()*(m-1) 

            
            for cnt in range(1,recall+1):
                process = multiprocessing.Process(target=fuc,args=(points,n,m))
                process.start()
                process.join(timeout=150)  # 0.1초 후에 프로세스가 종료되도록 대기

                if process.is_alive():
                    process.terminate()  # 프로세스를 종료
                    result = 'TLE'
                    break
                else:
                    cpu_time = fuc(points,n,m)[1]

                sum_time += cpu_time

            if cnt == recall: # 다 돌았을 때만 시간 저장 
                result = sum_time / recall

            series_list.append(pd.Series([n,m,result,str(fuc).split(' ')[1]]))
            print(n,m,result,str(fuc).split(' ')[1])

            df = pd.DataFrame(series_list)   
            df.columns = ['n','m','CPU TIME','def_name']

            # index= int(time.time())%10000
            csv_path = f"timedata/time_data_2.csv"
            df.to_csv(csv_path, index=False)
        




