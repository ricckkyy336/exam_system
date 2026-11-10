import urllib.request
import json

url = "http://127.0.0.1:5000/api/mark"
payload = {
    "student_id": 1,
    "exam_id": 1,
    "score": 75.0
}

req = urllib.request.Request(
    url, 
    data=json.dumps(payload).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)

try:
    with urllib.request.urlopen(req) as response:
        print("API Response:", response.read().decode('utf-8'))
except Exception as e:
    print("Error:", e)