from flask import Flask, request, jsonify, render_template
import requests, re, random, os
from dotenv import load_dotenv

load_dotenv()  # 로컬 테스트용

app = Flask(__name__)
bearer_token = os.environ.get("BEARER_TOKEN")

# 루트 경로: 브라우저 접속 시 HTML 페이지 렌더링
@app.route("/")
def home():
    return render_template("index.html")  # index.html이 프론트 페이지일 경우

# RT 랜덤 추첨 API
@app.route("/get_winners", methods=["POST"])
def get_winners():
    data = request.json
    tweet_url = data.get("tweet_url")
    n = int(data.get("num_winners", 1))

    match = re.search(r"/status/(\d+)", tweet_url)
    if not match:
        return jsonify({"error": "Invalid tweet URL"}), 400
    tweet_id = match.group(1)

    url = f"https://api.twitter.com/2/tweets/{tweet_id}/retweeted_by"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    params = {"max_results": 100}
    all_users = []
    next_token = None

    while True:
        if next_token:
            params["pagination_token"] = next_token
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            return jsonify({"error": response.json()}), response.status_code

        resp_data = response.json()
        users = resp_data.get("data", [])
        all_users.extend(users)

        meta = resp_data.get("meta", {})
        next_token = meta.get("next_token")
        if not next_token or len(all_users) >= 200:
            break

    if n > len(all_users):
        n = len(all_users)

    winners = random.sample(all_users, n)
    winner_list = [user["username"] for user in winners]

    return jsonify({"total_rt": len(all_users), "winners": winner_list})

if __name__ == "__main__":
    app.run(debug=True)
