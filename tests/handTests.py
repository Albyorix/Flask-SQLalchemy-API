from requests import get, post, put, delete

base_url = "http://127.0.0.1:5000/api/v1/"
url = base_url + "user"
params = {"name": "mike",
          "email": "mike@mike.com"}
r = post(url, json=params)
print r.status_code
print r.text