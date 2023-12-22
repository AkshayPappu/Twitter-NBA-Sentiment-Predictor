#FINAL FUNCTION TEMPLATE
import pandas as pd
import requests
from datetime import datetime
import joblib
import numpy as np
from textblob import TextBlob
from model import predict_winner as pw

#GENERATE TWITTER DATA
bearer_token = '' #Insert your twitter bearer token here
search_url = "https://api.twitter.com/2/tweets/search/recent"

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def extract_tweets_for_teams(url, team1, team2, end_date=None):
    #Converting end_date
    current_date = datetime.now().isoformat() + "Z"
    end_date_formatted = end_date if end_date else current_date

    # Loading Teams DataFrame
    teams_df = pd.read_csv(r"flask-server\player_data.csv")

    # Extract tweets for each team and its players
    tweets_data = []
    for selected_team in [team1, team2]:
        selected_team_row = teams_df.loc[teams_df['Team'] == selected_team]

        if not selected_team_row.empty:
            players = selected_team_row['Players'].values[0].split(',')

            # Get the last word of the team name
            last_word_team = selected_team.split()[-1]

            for player in players:
                query_params = {'query': f'({player} OR {last_word_team} {player}) -is:retweet lang:en', 'end_time': end_date_formatted, 'max_results': 10}
                response = requests.get(url, auth=bearer_oauth, params=query_params)
                if response.status_code == 200:
                    # Parse the JSON response
                    json_response = response.json()

                    # Extract tweets from the response and add to tweets_data
                    for tweet in json_response.get('data', []):
                        tweets_data.append({'Team': selected_team, 'Tweet': tweet.get('text', '')})
                else:
                    print(f"Error retrieving tweets for {selected_team}: {response.status_code}, {response.text}")
                    prediction = pw(team1, team2)
                    return prediction
    
    df = pd.DataFrame(tweets_data)

    return df

# Function to calculate sentiment score using TextBlob
def calculate_sentiment(tweet):
    analysis = TextBlob(tweet)
    return analysis.sentiment.polarity

#Function to format data to be input to model
def create_model_input(tweets_df, teams_df):
    # Create a duplicate DataFrame for editing
    edited_tweets_df = tweets_df.copy()

    # Add a new column 'Sentiment' to the edited DataFrame
    edited_tweets_df['Sentiment'] = edited_tweets_df['Tweet'].apply(calculate_sentiment)

    # Create a new DataFrame for pairs of teams
    team_changed = edited_tweets_df['Team'] != edited_tweets_df['Team'].shift(1)
    filtered_df = edited_tweets_df[team_changed]
    unique_team_list = filtered_df['Team'].tolist()
    unique_team_list
    team_pairs = [(unique_team_list[i], unique_team_list[i + 1]) for i in range(0, len(unique_team_list)-1, 2)]
    test_df = pd.DataFrame(index=range(len(team_pairs)), columns=['team1', 'team2', 'sentiment_score_team1', 'sentiment_score_team2'])

    # Split the 'Players' column into individual player names
    teams_df['Players'] = teams_df['Players'].apply(lambda x: x.split(','))

    # Initialize columns for each player
    num_players = 5
    for i in range(1, num_players + 1):
        test_df[f'team1p{i}score'] = 0.0
        test_df[f'team2p{i}score'] = 0.0

    # Columns for average player sentiments
    test_df['avg_player_sentiment_team1'] = 0.0
    test_df['avg_player_sentiment_team2'] = 0.0

    # Columns for count of positive, neutral, and negative tweets
    test_df['positive_tweets_team1'] = 0
    test_df['neutral_tweets_team1'] = 0
    test_df['negative_tweets_team1'] = 0
    test_df['positive_tweets_team2'] = 0
    test_df['neutral_tweets_team2'] = 0
    test_df['negative_tweets_team2'] = 0

    # Calculate sentiment scores for pairs of teams and update player columns
    for idx, (team1, team2) in enumerate(team_pairs):
        # Calculate the mean sentiment score for tweets mentioning each team
        team1_score = edited_tweets_df[edited_tweets_df['Team'] == team1]['Sentiment'].mean()
        team2_score = edited_tweets_df[edited_tweets_df['Team'] == team2]['Sentiment'].mean()

        test_df.at[idx, 'team1'] = team1
        test_df.at[idx, 'team2'] = team2
        test_df.at[idx, 'sentiment_score_team1'] = team1_score
        test_df.at[idx, 'sentiment_score_team2'] = team2_score

        # Update player columns for team1
        team1_players = teams_df.loc[teams_df['Team'] == team1, 'Players'].iloc[0]
        for i, player in enumerate(team1_players, start=1):
            player_score = edited_tweets_df[edited_tweets_df['Team'] == team1][edited_tweets_df['Tweet'].str.contains(player, case=False, na=False)]['Sentiment'].mean()
            test_df.at[idx, f'team1p{i}score'] = player_score if not pd.isnull(player_score) else 0

        # Update player columns for team2
        team2_players = teams_df.loc[teams_df['Team'] == team2, 'Players'].iloc[0]
        for i, player in enumerate(team2_players, start=1):
            player_score = edited_tweets_df[edited_tweets_df['Team'] == team2][edited_tweets_df['Tweet'].str.contains(player, case=False, na=False)]['Sentiment'].mean()
            test_df.at[idx, f'team2p{i}score'] = player_score if not pd.isnull(player_score) else 0

        # Calculate average player sentiments for team1 and team2
        avg_player_sentiment_team1 = test_df.loc[idx, [f'team1p{i}score' for i in range(1, num_players + 1)]].mean()
        avg_player_sentiment_team2 = test_df.loc[idx, [f'team2p{i}score' for i in range(1, num_players + 1)]].mean()

        test_df.at[idx, 'avg_player_sentiment_team1'] = avg_player_sentiment_team1
        test_df.at[idx, 'avg_player_sentiment_team2'] = avg_player_sentiment_team2

        # Count positive, neutral, and negative tweets for team1
        positive_tweets_team1 = edited_tweets_df[(edited_tweets_df['Team'] == team1) & (edited_tweets_df['Sentiment'] > 0)].shape[0]
        neutral_tweets_team1 = edited_tweets_df[(edited_tweets_df['Team'] == team1) & (edited_tweets_df['Sentiment'] == 0)].shape[0]
        negative_tweets_team1 = edited_tweets_df[(edited_tweets_df['Team'] == team1) & (edited_tweets_df['Sentiment'] < 0)].shape[0]

        test_df.at[idx, 'positive_tweets_team1'] = positive_tweets_team1
        test_df.at[idx, 'neutral_tweets_team1'] = neutral_tweets_team1
        test_df.at[idx, 'negative_tweets_team1'] = negative_tweets_team1

        # Count positive, neutral, and negative tweets for team2
        positive_tweets_team2 = edited_tweets_df[(edited_tweets_df['Team'] == team2) & (edited_tweets_df['Sentiment'] > 0)].shape[0]
        neutral_tweets_team2 = edited_tweets_df[(edited_tweets_df['Team'] == team2) & (edited_tweets_df['Sentiment'] == 0)].shape[0]
        negative_tweets_team2 = edited_tweets_df[(edited_tweets_df['Team'] == team2) & (edited_tweets_df['Sentiment'] < 0)].shape[0]

        test_df.at[idx, 'positive_tweets_team2'] = positive_tweets_team2
        test_df.at[idx, 'neutral_tweets_team2'] = neutral_tweets_team2
        test_df.at[idx, 'negative_tweets_team2'] = negative_tweets_team2

    return test_df

def predict_winner(team1, team2):
    #Get Tweets
    tweets_df = extract_tweets_for_teams(search_url, team1, team2)
    
    #Case fpr if Twitter API is down
    if isinstance(tweets_df, str):
        return tweets_df
    
    print(tweets_df)
    teams_df = pd.read_csv(r"flask-server\player_data.csv")

    #Format data for input into model
    test_df = create_model_input(tweets_df, teams_df)

    input_data = test_df.iloc[:8, 2:22]

    #Load model and predict
    loaded_rf = joblib.load(r'flask-server\random_forest_model.joblib')
    prediction = loaded_rf.predict(input_data)
    if prediction == 1:
        return f"{team1}"
    else:
        return f"{team2}"