import requests
import json

# 测试注册接口
url = "http://localhost:8000/api/users/register"
headers = {"Content-Type": "application/json"}
body = {"email": "test@example.com", "password": "password123", "confirm_password": "password123", "username": "testuser"}

response = requests.post(url, headers=headers, data=json.dumps(body))

print("Status Code:", response.status_code)
print("Response Body:", response.text)
