from flask import Flask, render_template, request
import plotly.graph_objects as go
import plotly.express as px
from load_data import top_10_men_singles, top_10_women_singles
app = Flask(__name__)

# Define a dictionary to store player statistics

player_statistics = {
    # "Player1": "Player A",
    # "Player2": "Player B",
    # "Nationality1": "Nation A",
    # "Nationality2": "Nation B",
    # "ScoreSet1": "21-18",
    # "ScoreSet2": "19-21",
    # "ScoreSet3": "21-17",
    # "LongestPoint1": 35,
    # "LongestPoint2": 42,
    # "MatchPoint1": 5,
    # "MatchPoint2": 7,
    # "HeadToHead": "Player A leads 5-2",
    # "Year": 2023,
}

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/type', methods=['GET', 'POST'])
def display():
    men_input_disabled = True  # Initially, the text input is disabled
    women_input_disabled = True
    if request.method == 'POST':
        selected_option = request.form.get('category')
        if selected_option == 'MS':
            men_input_disabled = False
        else:
            women_input_disabled = False
    return render_template('comparison.html', match_type=selected_option, men_input_disabled=men_input_disabled,
                           women_input_disabled=women_input_disabled,
                           men_players=top_10_men_singles, women_players=top_10_women_singles)


@app.route('/compare', methods=['GET', 'POST'])
def display_stats():
    def visualize(dataframe):
        pass

    player_men_1 = request.form.get('playerm1')
    player_men_2 = request.form.get('playerm2')
    player_women_1 = request.form.get('playerw1')
    player_women_2 = request.form.get('playerw2')


    # stats_player1 = player_statistics.get(player1, {})
    # stats_player2 = player_statistics.get(player2, {})

    # Extracting the statistics and player info
    # player1_stats = [stats_player1['Stat1'], stats_player1['Stat2']]
    # player2_stats = [stats_player2['Stat1'], stats_player2['Stat2']]
    # metric_labels = ['Stat1', 'Stat2']

    # Create the bar chart using Plotly
    # fig = go.Figure()
    #
    # fig.add_trace(go.Bar(
    #     x=[player1, player2],
    #     y=player1_stats,
    #     name=player1,
    #     text=['Country: ' + stats_player1['Country'] + '<br>Category: ' + stats_player1['Category']] * len(metric_labels),
    #     hoverinfo='text+y',
    #     offsetgroup=0
    # ))
    #
    # fig.add_trace(go.Bar(
    #     x=[player1, player2],
    #     y=player2_stats,
    #     name=player2,
    #     text=['Country: ' + stats_player2['Country'] + '<br>Category: ' + stats_player2['Category']] * len(metric_labels),
    #     hoverinfo='text+y',
    #     offsetgroup=1
    # ))
    #
    # fig.update_layout(
    #     title='Comparison of Player Statistics',
    #     xaxis=dict(title='Players'),
    #     yaxis=dict(title='Statistics'),
    #     barmode='group'
    # )

    # plot_html = fig.to_html(full_html=False)

    return render_template('displayStat.html')

if __name__ == '__main__':
    app.run(debug=True)
