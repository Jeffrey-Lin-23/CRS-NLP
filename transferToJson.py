import pandas as pd
import json


df1 = pd.read_csv('summary(2).csv',encoding='utf-8')
df2 = pd.read_csv('try11.csv',encoding='utf-8',header=None)
#df3 = pd.read_csv('finalresult.csv',encoding='utf-8')
df4 = pd.read_csv('compare 2.csv',encoding='utf-8')

print(df4)
xs = []
ys = []
df2.columns = ["X","Y"]
for i,values in df2.iterrows():
    xs.append(values["X"])
    ys.append(values["Y"])
'''
conDic = {}
for i,values in df3.iterrows():
    name = str(values["Name"]).split(" ")
    idx = name[0]
    content = values["Content"]
    conDic[idx] = content
'''
    
graphs = {"nodes":[],"edges":[]}

for i,values in df1.iterrows():
    name = values["Name"]
    idx = values["ID"].replace("'",'')
    faculty = values["Faculty"]
    '''
    if idx in conDic:
        content = conDic[idx]
    else:
        content = conDic[idx[1:]]
    '''
    #outline_url = 
    graphs["nodes"].append({"id":idx,
                             "name":name,
                             "faculty":faculty,
                             "x":xs[i],
                             "y":ys[i],
                             "outline_url":values["url"],
                             })

columns = df4.columns
new_columns = []
for c in columns:
    if c[0] == '0':
        c = c[1:]
    new_columns.append(c)
#df4.columns = new_columns

print(len(new_columns))
edges = []
for i,values in df4.iterrows():
    source = columns[i+1]
    
    for j,target in enumerate(columns[1:]):
        v = values[target]
        if target != source and v>=0.4:

            if [source,target] not in edges and [target ,source] not in edges:
                graphs["edges"].append({"source":source,
                                 "target":target,
                                 "value":v,
                                 "type":"normal"})
                edges.append([source,target])


fr = open("finalRequest .csv","r")
Requests = []
lines = fr.readlines()
for line in lines[1:]:
    line = line.split(",")[:-1]
    line = [l.replace("'","") for l in line]

    for i in range(len(line)-1):
        Requests.append([line[0],line[i+1]])
fr.close()

for edge in graphs["edges"]:
    st = [edge["source"],edge["target"]]
    ts = [edge["target"],edge["source"]]
    if st in Requests or ts in Requests:
        edge["type"] = "request"


fr = open("Anti-request .csv","r")
Requests = []
lines = fr.readlines()
for line in lines[1:]:
    line = line.split(",")[:-1]
    line = [l.replace("'","") for l in line]

    for i in range(len(line)-1):
        Requests.append([line[0],line[i+1]])
fr.close()

for edge in graphs["edges"]:
    st = [edge["source"],edge["target"]]
    ts = [edge["target"],edge["source"]]
    if st in Requests or ts in Requests:
        edge["type"] = "anti-request"

print(len(graphs["nodes"]))
print(len(graphs["edges"]))
with open("data.json",'w',encoding='utf-8') as json_file:
    json.dump(graphs,json_file,ensure_ascii=False,indent=2)

