import requests as req

SERVER_IP = 'aibg2022.com:8081'
CONNECTION_JSON = {
    'username': 'JutricKafica',
    'password': 'q8K^Hx9%L6'
}

url = lambda _url : f'http://{SERVER_IP}/{_url}'

resp = req.post(url('user/login'), json=CONNECTION_JSON)

print(resp.text)