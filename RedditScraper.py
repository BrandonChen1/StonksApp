import requests

url = "http://reddit.com"
response = requests.get(url)

print(response.status_code)
print(response.text[:500])