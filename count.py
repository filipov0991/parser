import pandas as pd

df = pd.read_csv("C:\Users\User\Desktop\\test\\data.csv")

c = df['Имя Фамилия']

f = []
c1= []
d = {}
for i in c:
    if len(i)>1:
        f.append(i.split())
for i in f:
    c1.append(i[1][0])
for i in c1:
    d[i] = (c1.count(i))

ddf = pd.DataFrame.from_dict(d,orient='index').transpose()
ddf = ddf.fillna(method='ffill')