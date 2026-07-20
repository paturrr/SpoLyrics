import requests
resp = requests.get('https://lrclib.net/api/search', params={'q': 'Ribuan Memori'})
print(resp.json())
