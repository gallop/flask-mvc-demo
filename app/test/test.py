import json


list = [1, 2, 3, 4, 5]
tt = json.dumps(list)
print(tt)
aa= eval(tt)
print(type(aa))
print('aa=', aa)