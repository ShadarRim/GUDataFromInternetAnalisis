import requests
import json
from pprint import pprint


owner = 'ShadarRim'
response = requests.get(f'https://api.github.com/users/{owner}/repos')

repolist = []
if response.ok:
    data = json.loads(response.text)
    with open('gitdata.txt', 'w') as f:
        json.dump(data, f)
    for elem in data:
        repolist.append(elem['name'])
else:
    print('Mistake')

print(f'Список репозиториев для пользовался {owner}: {repolist}')