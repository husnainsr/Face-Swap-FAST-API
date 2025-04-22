# Save as test_upload.py
import requests

url = "http://localhost:8000/faceswap"
token = "166d23d5-338e-4831-ac65-01e3706b4849"
source_path = r"C:\Users\Lenovo\Pictures\dp.jpg"
target_path = r"C:\Users\Lenovo\Pictures\model2.jpg"

headers = {
    "X-API-Key": token
}

with open(source_path, "rb") as source_file, open(target_path, "rb") as target_file:
    files = {
        "source_image": ("dp.jpg", source_file, "image/jpeg"),
        "target_image": ("model2.jpg", target_file, "image/jpeg")
    }
    
    response = requests.post(url, headers=headers, files=files)
    
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")