import urllib.request
import urllib.error
import json
import random

BASE_URL = "http://localhost/api"

GAMES = [
    {"name": "Valorant", "description": "Tactical shooter"},
    {"name": "League of Legends", "description": "MOBA game"},
    {"name": "Apex Legends", "description": "Battle Royale"},
    {"name": "Minecraft", "description": "Sandbox game"},
    {"name": "Fortnite", "description": "Battle Royale"},
    {"name": "CS:GO", "description": "Tactical shooter"},
    {"name": "Overwatch 2", "description": "Hero shooter"},
    {"name": "Dota 2", "description": "MOBA game"},
    {"name": "Grand Theft Auto V", "description": "Open world"},
    {"name": "Elden Ring", "description": "Action RPG"}
]

ADJECTIVES = ["Pro", "Chill", "Ranked", "Casual", "Late Night", "Speedrun", "100%", "No Hit", "Practice", "Tournament"]
NOUNS = ["Vibes", "Grind", "Climb", "Gameplay", "Stream", "Session", "Fun", "Action"]

def post_json(url, data):
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Error {e.code} on {url}: {e.read().decode()}")
        return None

def main():
    print("Seeding Games...")
    game_data = []
    for game in GAMES:
        res = post_json(f"{BASE_URL}/games", game)
        if res:
            game_data.append(res)
        else:
            # Maybe already exists, fetch it
            try:
                with urllib.request.urlopen(f"{BASE_URL}/games") as response:
                    all_games = json.loads(response.read().decode())
                    for g in all_games:
                        if g['name'] == game['name']:
                            game_data.append(g)
            except Exception:
                pass
            
    print("Seeding 50 Users...")
    users = []
    for i in range(1, 51):
        username = f"streamer_{i}_{random.randint(1000, 9999)}"
        res = post_json(f"{BASE_URL}/users/register", {
            "username": username,
            "email": f"{username}@example.com",
            "password": "password123"
        })
        if res:
            users.append(res)
            
    print("Seeding 20 Active Streams...")
    for i in range(20):
        if not users or not game_data:
            break
        user = random.choice(users)
        game = random.choice(game_data)
        title = f"{random.choice(ADJECTIVES)} {game['name']} {random.choice(NOUNS)}!"
        post_json(f"{BASE_URL}/streams", {
            "streamer_id": user["username"],
            "game_id": game["id"],
            "game_name": game["name"],
            "title": title
        })
        
    print("Done! Dashboard should now be populated.")

if __name__ == "__main__":
    main()
