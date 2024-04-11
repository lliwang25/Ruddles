from fastapi import FastAPI
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
import openai
import httpx

app = FastAPI()

@app.get("/riddle/{player_name}")
async def get_riddle(player_name: str):
    # Find player by name
    player_dict = players.get_players()
    player = [p for p in player_dict if player_name.lower() in p['full_name'].lower()]
    if not player:
        return {"error": "Player not found"}
    player = player[0]

    # Fetch career stats for the player
    career = playercareerstats.PlayerCareerStats(player_id=player['id'])
    career_df = career.get_data_frames()[0]
    latest_season = career_df.iloc[-1]

    # Generate a riddle using OpenAI
    prompt = f"Create a riddle about an NBA player who scored {latest_season['PTS']} points and played for {latest_season['TEAM_ABBREVIATION']} in their last season."
    response = await httpx.post(
        'https://api.openai.com/v1/engines/text-davinci-002/completions',
        headers={'Authorization': f'Bearer your_openai_api_key'},
        json={'prompt': prompt, 'max_tokens': 150}
    )
    riddle = response.json()['choices'][0]['text'].strip()

    return {"riddle": riddle}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
