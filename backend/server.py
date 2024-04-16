from flask import Flask, jsonify
import random
import openai
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog

app = Flask(__name__)

def get_random_player():
    # Fetch all players who played in the current season
    active_players = players.get_active_players()
    random_player = random.choice(active_players)
    return random_player

def get_player_stats(player_id):
    # Fetch the game log for the player for the current season
    game_log = playergamelog.PlayerGameLog(player_id=player_id, season='2024')
    stats = game_log.get_data_frames()[0]
    return stats

def generate_riddles(player_info, stats):
    prompt = f"Create 6 riddles based on the following NBA player's 2024 season stats: {player_info}, {stats}"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150
    )
    riddles = response.choices[0].text.strip().split('\n')
    return riddles[:6]

@app.route("/riddle")
def riddle():
    player = get_random_player()
    stats = get_player_stats(player['id'])
    player_info = f"{player['full_name']} stats"
    riddles = generate_riddles(player_info, stats.to_dict(orient='records')[0])
    # Include the player's name in the response for validation on the frontend
    return jsonify({"riddles": riddles, "playerName": player['full_name']})


if __name__ == "__main__":
    app.run(debug=True)
