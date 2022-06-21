import requests

data = requests.get("http://127.0.0.1:8000/addressBook")

jsondata= data.json()
d =[i for i in jsondata if i['long']>=12 ]
print(d)
