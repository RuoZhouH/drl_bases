
import pandas as pd

train={'K001':[[1,2,3],[4,5,6],[7,8,9]],'K002':[[4,5,8],[5,5,6],[4,3,6]] }
df1=pd.DataFrame(columns=('a','b','c'))
for i in train.keys():
    for h in range(len(train[i])):
        data1=train[i][h]
        data2=[{'a':data1[0],'b':data1[1],'c':data1[2]}]
        df2=pd.DataFrame(data2,index=[i],columns=('a','b','c'))
        df1=df1.append(df2)
print(df1)
