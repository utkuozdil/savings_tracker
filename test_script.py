import httpx
import time

BASE_URL = "http://localhost:8000"

def wait_for_server():
    max_retries = 5
    retry_delay = 2
    
    for i in range(max_retries):
        try:
            response = httpx.get(f"{BASE_URL}/savings/")
            if response.status_code == 200:
                print("Server is ready!")
                return True
        except httpx.ConnectError:
            if i < max_retries - 1:
                print(f"Waiting for server... (attempt {i + 1}/{max_retries})")
                time.sleep(retry_delay)
            else:
                print("Could not connect to server. Make sure it's running.")
                return False

if not wait_for_server():
    exit(1)

# 1. Create a new saving
saving_data = {
    "date": "2024-05-24",
    "amount": 12.5,
    "category": "gold",
    "notes": "Test from script"
}

try:
    response = httpx.post(f"{BASE_URL}/savings/", json=saving_data)
    print("📌 POST Response:", response.json())
    saving_id = response.json().get("id")

    # 2. Get all savings
    response = httpx.get(f"{BASE_URL}/savings/")
    print("📋 GET All:", response.json())

    # 3. Get a specific saving
    if saving_id:
        response = httpx.get(f"{BASE_URL}/savings/{saving_id}")
        print("🔎 GET by ID:", response.json())

    # 4. Update the saving
    updated_data = {
        "date": "2024-05-24",
        "amount": 15.0,
        "category": "gold",
        "notes": "Updated from script"
    }
    response = httpx.put(f"{BASE_URL}/savings/{saving_id}", json=updated_data)
    print("✏️ PUT Response:", response.json())

    # 5. Get summary
    response = httpx.get(f"{BASE_URL}/summary/")
    print("📊 Summary:", response.json())

    # 6. Delete the saving
    response = httpx.delete(f"{BASE_URL}/savings/{saving_id}")
    print("🗑 DELETE Response:", response.json())

    # 7. Confirm deletion
    response = httpx.get(f"{BASE_URL}/savings/{saving_id}")
    print("❌ Confirm Deletion:", response.json())

except httpx.ConnectError as e:
    print(f"Connection error: {e}")
    print("Make sure the Docker container is running and the port is correctly mapped.")
except Exception as e:
    print(f"An error occurred: {e}")
