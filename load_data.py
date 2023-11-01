import json
import pandas as pd

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


# Function to split match score
def split_score(df, winner):
    num_rows = df.shape[0]
    P1_T1_S1, P1_T1_S2, P1_T1_S3 = [[21] * num_rows for _ in range(3)]
    P2_T2_S1, P2_T2_S2, P2_T2_S3 = [[0] * num_rows for _ in range(3)]
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


df = split_score(df, 1)
# Replace specific values in the DataFrame
df = df.replace({'duration:': 0, '-': 0})
# Change data type to int
df = df.astype({"T": int, "P1/T1-TP": int, "P2/T2-TP": int, "P1/T1-L": int, "P2/T2-L": int, "P1/T1-W": int,
                "P2/T2-W": int, "P1/T1-GP": int, "P2/T2-GP": int, "P1/T1-LP": int, "P2/T2-LP": int, "P1-H2H": int,
                "P2-H2H": int, "P1/T1-S1": int, "P2/T2-S1": int, "P1/T1-S2": int, "P2/T2-S2": int, "P1/T1-S3": int,
                "P2/T2-S3": int, 'P1/T1-S': int, 'P2/T2-S': int})

set_of_players = set(df['P1'].unique()).union(set(df['P2'].unique()))


def group_player_winratio_by_year(df, player):
    # Filter the DataFrame for matches where the player won (P1) or lost (P2)
    df_player_win = df[df['P1'].str.lower() == player.lower()]
    df_player_lose = df[df['P2'].str.lower() == player.lower()]

    # Group and count the wins and losses by year
    win_by_year = df_player_win.groupby(['Y'])['P1'].count().reset_index()
    lose_by_year = df_player_lose.groupby(['Y'])['P2'].count().reset_index()

    # Merge the win and loss DataFrames on 'Y' (Year) with an outer join to include all years
    merge_df = win_by_year.merge(lose_by_year, on='Y', how='outer')

    # Fill missing values with 0 to handle years with no wins or losses
    merge_df = merge_df.fillna(0)

    # Calculate the win-loss ratio and total match play for each year
    merge_df['%win_loss'] = round(merge_df['P1'] / (merge_df['P1'] + merge_df['P2']) * 100, 2)
    merge_df['Match play'] = merge_df['P1'] + merge_df['P2']
    merge_df = merge_df.astype({'Match play': int})
    # Return a DataFrame with the desired columns
    return merge_df[['Y', '%win_loss', 'Match play']]


def group_player_matchscore_by_year(df, player):
    # Filter the DataFrame for matches where the player won (P1) or lost (P2)
    df_player_win = df[df['P1'].str.lower() == player.lower()]
    df_player_lose = df[df['P2'].str.lower() == player.lower()]

    # Group and sum the point scores for each set by year for wins and losses
    point_in_win_match_by_year = df_player_win.groupby(['Y'])[['P1/T1-S1', 'P1/T1-S2', 'P1/T1-S3']].sum().reset_index()
    point_in_lose_match_by_year = df_player_lose.groupby(['Y'])[
        ['P2/T2-S1', 'P2/T2-S2', 'P2/T2-S3']].sum().reset_index()

    opponent_point_in_win_match_by_year = df_player_win.groupby(['Y'])[
        ['P2/T2-S1', 'P2/T2-S2', 'P2/T2-S3']].sum().reset_index()
    opponent_point_in_lose_match_by_year = df_player_lose.groupby(['Y'])[
        ['P1/T1-S1', 'P1/T1-S2', 'P1/T1-S3']].sum().reset_index()
    # Merge the point scores DataFrames on 'Y' with an outer join to ensure all years are included
    merge_df = point_in_win_match_by_year.merge(point_in_lose_match_by_year, on='Y', how='outer')
    merge_opponent_df = opponent_point_in_win_match_by_year.merge(opponent_point_in_lose_match_by_year, on='Y',
                                                                  how='outer')
    player_vs_opponent = merge_df.merge(merge_opponent_df, on='Y', how='outer')
    # Fill missing values with 0 to handle years with no wins or losses
    player_vs_opponent = player_vs_opponent.fillna(0)

    # Group and count the total number of matches played by year for wins and losses
    total_match_win = df_player_win.groupby(['Y'])['Winner'].count().reset_index()
    total_match_lose = df_player_lose.groupby(['Y'])['Winner'].count().reset_index()

    # Merge the match counts DataFrames on 'Y' with an outer join to ensure all years are included
    merge_match = total_match_win.merge(total_match_lose, on='Y', how='outer')

    # Fill missing values with 0 to handle years with no wins or losses
    merge_match = merge_match.fillna(0)

    # Calculate the total match play for each year and replace 0 with 1 to avoid division by zero
    merge_match['MatchPlay'] = merge_match['Winner_x'] + merge_match['Winner_y']
    merge_match['MatchPlay'] = merge_match['MatchPlay'].replace(0, 1)

    # Calculate the total scores for each set by adding wins and losses
    player_vs_opponent['set1'], player_vs_opponent['set1_op'] = player_vs_opponent['P1/T1-S1_x'] + player_vs_opponent[
        'P2/T2-S1_x'], player_vs_opponent['P1/T1-S1_y'] + player_vs_opponent['P2/T2-S1_y']
    player_vs_opponent['set2'], player_vs_opponent['set2_op'] = player_vs_opponent['P1/T1-S2_x'] + player_vs_opponent[
        'P2/T2-S2_x'], player_vs_opponent['P1/T1-S2_y'] + player_vs_opponent['P2/T2-S2_y']
    player_vs_opponent['set3'], player_vs_opponent['set3_op'] = player_vs_opponent['P1/T1-S3_x'] + player_vs_opponent[
        'P2/T2-S3_x'], player_vs_opponent['P1/T1-S3_y'] + player_vs_opponent['P2/T2-S3_y']

    # Normalize the set scores by dividing by the total match play
    player_vs_opponent.iloc[:, 1:] = player_vs_opponent.iloc[:, 1:].div(merge_match['MatchPlay'].values, axis=0).round(2)
    return player_vs_opponent[['Y', 'set1', 'set2', 'set3', 'set1_op', 'set2_op', 'set3_op']]


def match_duration_by_year(df, player):
    df_player_win = df[df['P1'].str.lower() == player.lower()]
    df_player_lose = df[df['P2'].str.lower() == player.lower()]
    win_match_duration = df_player_win.groupby(['Y'])[['T']].sum().reset_index()
    loss_match_duration = df_player_lose.groupby(['Y'])[['T']].sum().reset_index()
    merge_df = win_match_duration.merge(loss_match_duration, on='Y', how='outer')

    # Fill missing values with 0 to handle years with no wins or losses
    merge_df = merge_df.fillna(0)

    # Group and count the total number of matches played by year for wins and losses
    total_match_win = df_player_win.groupby(['Y'])['Winner'].count().reset_index()
    total_match_lose = df_player_lose.groupby(['Y'])['Winner'].count().reset_index()

    # Merge the match counts DataFrames on 'Y' with an outer join to ensure all years are included
    merge_match = total_match_win.merge(total_match_lose, on='Y', how='outer')

    # Fill missing values with 0 to handle years with no wins or losses
    merge_match = merge_match.fillna(0)

    # Calculate the total match play for each year and replace 0 with 1 to avoid division by zero
    merge_match['MatchPlay'] = merge_match['Winner_x'] + merge_match['Winner_y']
    merge_match['MatchPlay'] = merge_match['MatchPlay'].replace(0, 1)

    merge_df['Duration'] = merge_df['T_x'] + merge_df['T_y']
    merge_df.iloc[:, 1:] = merge_df.iloc[:, 1:].div(merge_match['MatchPlay'].values, axis=0).round(2)
    return merge_df[['Y', 'Duration']]

