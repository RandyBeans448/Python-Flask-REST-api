import requests

BASE = "http://127.0.0.1:5000/"

data = [
    {"name": "The lord of the rings the two towers" ,"likes": 1000000, "views": 1000000},
    {"name": "The lord of the rings the fellowship of the ring" ,"likes": 1000000, "views": 1000000},
    {"name": "Beauty and the beast" ,"likes": 40000, "views": 40000}
]

for i in range(len(data)):
    response = requests.put(BASE + "/video/" + str(i), data[i])
    print(response.json())


input()
response = requests.get(BASE + "/video/10")
print(response.json())
