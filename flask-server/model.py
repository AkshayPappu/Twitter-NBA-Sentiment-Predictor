#FINAL FUNCTION TEMPLATE
import pandas as pd
import random
import joblib

# Helper function to generate fake data for a team
def generate_fake_team_data(team_name):
    pos_count = random.randint(50, 150)
    neg_count = random.randint(0, 50)
    neu_count = 200 - pos_count - neg_count

    # Adjusting team's polarity based on tweet sentiment
    team_polarity = (pos_count - neg_count) / 200  # Normalized to [-1, 1]

    players_polarity = [random.uniform(-1, 1) for _ in range(5)]
    avg_player_polarity = sum(players_polarity) / len(players_polarity)

    data = {
        f"{team_name}_Polarity": team_polarity,
        f"{team_name}_#pos": pos_count,
        f"{team_name}_#neu": neu_count,
        f"{team_name}_#neg": neg_count,
        f"{team_name}_Player_Polarity_1": players_polarity[0],
        f"{team_name}_Player_Polarity_2": players_polarity[1],
        f"{team_name}_Player_Polarity_3": players_polarity[2],
        f"{team_name}_Player_Polarity_4": players_polarity[3],
        f"{team_name}_Player_Polarity_5": players_polarity[4],
        f"{team_name}_Avg_Player_Polarity": avg_player_polarity
    }

    return data

def predict_winner(team1, team2):
    
    #replace with twitter data extraction code and output a pd df at the end
    team1_data = generate_fake_team_data(team1)
    team2_data = generate_fake_team_data(team2)
    combined_data = {**team1_data, **team2_data, 'Team1_Name': f"{team1}", 'Team2_Name': f"{team2}"}
    combined_data = pd.DataFrame(combined_data, index=[1])

    #prepare twitter data for input to model
    input_data = combined_data.iloc[0, :20].values.reshape(1, -1)

    #load the trained model and make a prediction
    loaded_rf = joblib.load(r'flask-server\random_forest_model.joblib')
    prediction = loaded_rf.predict(input_data)
    if prediction == 1:
        return f"{team1}"
    else:
        return f"{team2}"