import requests

token = '8885278750:AAHZKJVzHSvCZceWnCzyv1cc8Qy_NLqVZis'

response = requests.get(f'https://api.telegram.org/bot{token}/getUpdates')
print(response.json())