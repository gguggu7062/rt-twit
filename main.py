import requests
import re
import random

# 1. Bearer Token
bearer_token = "AAAAAAAAAAAAAAAAAAAAADfP4AEAAAAAKsA93N9vq46hejCySrmmbiOP2Wg%3D75mSYOvnGNlY1kUofIQIQIoVfQjqK2dQLAJJPARB5Y6tD8ZLc6"

# 2. 트윗 URL 입력
tweet_url = input("트윗 URL을 입력하세요: ").strip()

# 3. URL에서 트윗 ID 추출
match = re.search(r"/status/(\d+)", tweet_url)
if match:
    tweet_id = match.group(1)
else:
    raise ValueError("트윗 URL에서 ID를 찾을 수 없습니다.")

# 4. API URL (최대 200명만 가져오기)
url = f"https://api.twitter.com/2/tweets/{tweet_id}/retweeted_by"

# 5. 헤더 설정
headers = {
    "Authorization": f"Bearer {bearer_token}"
}

# 6. 요청 파라미터
params = {"max_results": 100}  # 한 번에 최대 100명
all_users = []
next_token = None

while True:
    if next_token:
        params["pagination_token"] = next_token
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        break
    
    data = response.json()
    users = data.get("data", [])
    all_users.extend(users)
    
    meta = data.get("meta", {})
    next_token = meta.get("next_token")
    
    # 최대 200명까지만 가져오기
    if len(all_users) >= 200:
        all_users = all_users[:200]
        break
    
