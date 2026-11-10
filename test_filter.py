import urllib.request

url = "http://127.0.0.1:5000/api/marks?student_id=1"

try:
    with urllib.request.urlopen(url) as response:
        print("Filtered Marks Result:\n", response.read().decode('utf-8'))
except Exception as e:
    print("Error:", e)