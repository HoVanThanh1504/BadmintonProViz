import json
import pandas as pd
import numpy as np
import plotly.express as px

# Load data from JSON file
path = './tournament_dataset.json'
with open(path) as json_file:
    data = json.load(json_file)

# Extract values from JSON data
match_statistic = []
for line in data:
    for key, value in line.items():
        match_statistic.append(value)

# Create a DataFrame from the extracted data
df = pd.DataFrame.from_dict(match_statistic)
df.set_index('Y')

# Function to split match score
def split_score(df, winner):
    num_rows = df.shape[0]
    P1_T1_S1, P2_T2_S1, P1_T1_S2, P2_T2_S2, P1_T1_S3, P2_T2_S3 = [[0] * num_rows for _ in range(6)]
    i = 0
    for row in df.MatchScore: # row: 21-12, 12-21, 21-7
        row = row.split(",")
        if len(row) == 1:
            i += 1
        elif len(row) == 2:
            set1 = row[0].strip().split("-")
            P1_T1_S1[i] = set1[0].strip()
            P2_T2_S1[i] = set1[1].strip()
            if row[1].strip() != "-":
                set2 = row[1].strip().split("-")
                P1_T1_S2[i] = set2[0].strip()
                P2_T2_S2[i] = set2[1].strip()
            i += 1
        else:
            set1 = row[0].strip().split("-")
            P1_T1_S1[i] = set1[0].strip()
            P2_T2_S1[i] = set1[1].strip()

            set2 = row[1].strip().split("-")
            P1_T1_S2[i] = set2[0].strip()
            P2_T2_S2[i] = set2[1].strip()
            if row[2].strip() != "-":
                set3 = row[2].strip().split("-")
                P1_T1_S3[i] = set3[0].strip()
                P2_T2_S3[i] = set3[1].strip()
            i += 1
    df['P1/T1-S1'], df['P2/T2-S1'] = P1_T1_S1, P2_T2_S1
    df['P1/T1-S2'], df['P2/T2-S2'] = P1_T1_S2, P2_T2_S2
    df['P1/T1-S3'], df['P2/T2-S3'] = P1_T1_S3, P2_T2_S3
    df['Winner'] = winner
    df.drop(columns='MatchScore', inplace=True)
    return df

# Convert certain columns to integer type
df = split_score(df, 1)
# Replace specific values in the DataFrame
df = df.replace({'duration:': 0, '-': 0})
# Change data type to int
df = df.astype({"T": int, "P1/T1-TP": int, "P2/T2-TP": int, "P1/T1-L": int, "P2/T2-L": int, "P1/T1-W": int,
                "P2/T2-W": int, "P1/T1-GP": int, "P2/T2-GP": int, "P1/T1-LP": int, "P2/T2-LP": int, "P1-H2H": int,
                "P2-H2H": int, "P1/T1-S1": int, "P2/T2-S1": int, "P1/T1-S2": int, "P2/T2-S2": int, "P1/T1-S3": int,
                "P2/T2-S3": int, 'P1/T1-S': int, 'P2/T2-S': int})

top_10_men_singles = ['Viktor AXELSEN', 'Kento MOMOTA', 'Anders ANTONSEN', 'CHOU Tien Chen', 'Anthony Sinisuka GINTING', 'CHEN Long', 'LEE Zii Jia', 'Jonatan CHRISTIE', 'NG Ka Long Angus', 'KIDAMBI Srikanth']
top_10_women_singles = ['TAI Tzu Ying', 'Akane YAMAGUCHI', 'CHEN Yu Fei', 'AN Se Young', 'Nozomi OKUHARA', 'Carolina MARIN', 'PUSARLA V. Sindhu', 'Ratchanok INTANON', 'HE Bing Jiao', 'Pornpawee CHOCHUWONG']
df_men_singles = df[(df['P1'].str.lower()).isin(list(map(lambda x: x.lower(), top_10_men_singles)))]
df_women_singles = df[(df['P1'].str.lower()).isin(list(map(lambda x: x.lower(), top_10_women_singles)))]


def compare_2_single_players(dataframe, player1, player2):
    df_2_players = dataframe[((dataframe['P1'].str.lower() == player1.lower()) &
                             (dataframe['P2'].str.lower() == player2.lower())) |
                             ((dataframe['P2'].str.lower() == player1.lower()) &
                             (dataframe['P1'].str.lower() == player2.lower()))]
    year = df_2_players.index
    nation1, nation2 = df_2_players[df['P1'] == player1]['P1-C'], df_2_players[df['P2'] == player2]['P2-C']
    player1_h2h, player2_h2h = df_2_players['P1-H2H'], df_2_players['P2-H2H']
    scores = dataframe['P1/T1-S1', 'P2/T2-S1', 'P1/T1-S2', 'P2/T2-S2', 'P1/T1-S3', 'P2/T2-S3']
    longest_point = dataframe['P1/T1-LP', 'P2/T2-LP']
    match_point = dataframe['P1/T1-GP', 'P2/T2-GP']
    return year, nation1, nation2, player1_h2h, player2_h2h, scores, longest_point, match_point

