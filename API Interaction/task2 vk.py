import requests
import json
from pprint import pprint

#получить токен можно, создав собственое приложение в API
#scope = 65536 при запросе позволяет получить токен без ограничения, scope = 2 - доступ к друзьям пользователя, запрос списка друзей он-лайн соответственно scope = 65538

#сам токен удалён, чтобы не выкладывать в сеть

ac_token = 'здесь должен быть ваш токен'
response = requests.get(f'https://api.vk.com/method/friends.getOnline?v=5.52&access_token={ac_token}')

repolist = []
if response.ok:
    data = json.loads(response.text)
    pprint(data)
else:
    print('Mistake')
