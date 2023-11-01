from flask import Flask, render_template, request
import plotly.graph_objects as go
import plotly.express as px
from load_data import set_of_players, df, group_player_winratio_by_year, group_player_matchscore_by_year, match_duration_by_year
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', players=set_of_players)


@app.route('/display', methods=['GET', 'POST'])
def display_stats():
    player = request.form.get('player')

    win_ratio = group_player_winratio_by_year(df, player)
    match_score = group_player_matchscore_by_year(df, player)
    match_duration = match_duration_by_year(df, player)

    fig_win_loss = go.Figure()
    fig_win_loss.add_trace(go.Scatter(x=win_ratio['Y'], y=win_ratio['%win_loss'], mode='lines+markers', name='% Win',
                                      text=win_ratio["Match play"], textposition="top center",
                                      hovertext=[f'Year: {y}<br>%win_loss: {win_loss}<br>Match play: {match_play}' for
                                                 y, win_loss, match_play in
                                                 zip(win_ratio['Y'], win_ratio['%win_loss'], win_ratio['Match play'])]
                                      ))
    fig_win_loss.update_layout(title=dict(text='Win-Loss Percentage Over Time', x=0.5, y=0.95),
                               xaxis_title='Year', yaxis_title='% Win-Loss')

    # fig_points_scored = go.Figure()

    # fig_points_scored.add_trace(go.Scatter(x=match_score['Y'], y=match_score['set1'], mode='lines+markers', name='Set 1'))
    # fig_points_scored.add_trace(go.Scatter(x=match_score['Y'], y=match_score['set2'], mode='lines+markers', name='Set 2'))
    # fig_points_scored.add_trace(go.Scatter(x=match_score['Y'], y=match_score['set3'], mode='lines+markers', name='Set 3'))
    #
    # # Add lines for opponent's set scores
    # fig_points_scored.add_trace(go.Scatter(x=match_score['Y'], y=match_score['set1_op'], mode='lines+markers',
    #                             name='Opponent Set 1'))
    # fig_points_scored.add_trace(go.Scatter(x=match_score['Y'], y=match_score['set2_op'], mode='lines+markers',
    #                             name='Opponent Set 2'))
    # fig_points_scored.add_trace(go.Scatter(x=match_score['Y'], y=match_score['set3_op'], mode='lines+markers',
    #                             name='Opponent Set 3'))

    # Customize the layout
    # fig_points_scored.update_layout(
    #     title='Player vs. Opponent Set Scores Over Time',
    #     xaxis_title='Year',
    #     yaxis_title='Score',
    # )
    fig_points_scored = go.Figure()

    # Add bars for player's set scores
    fig_points_scored.add_trace(go.Bar(x=match_score['Y'], y=match_score['set1'], name='Set 1 (Player)'))

    fig_points_scored.add_trace(go.Bar(x=match_score['Y'], y=match_score['set2'], name='Set 2 (Player)'))

    fig_points_scored.add_trace(go.Bar(x=match_score['Y'], y=match_score['set3'], name='Set 3 (Player)'))

    # Add bars for opponent's set scores
    fig_points_scored.add_trace(go.Bar(x=match_score['Y'], y=match_score['set1_op'], name='Set 1 (Opponent)'))

    fig_points_scored.add_trace(go.Bar(x=match_score['Y'], y=match_score['set2_op'], name='Set 2 (Opponent)'))
    fig_points_scored.add_trace(go.Bar(x=match_score['Y'], y=match_score['set3_op'], name='Set 3 (Opponent)'))

    # Customize the layout
    fig_points_scored.update_layout(
        title=dict(text='Player vs. Opponent Set Scores Over Time', x=0.5, y=0.95), xaxis_title='Year',
        yaxis_title='Score', barmode='group'  # Display bars grouped for each year
    )

    fig_match_duration = go.Figure()
    fig_match_duration.add_trace(go.Scatter(x=match_duration['Y'], y=match_duration['Duration'], mode='lines+markers',
                                            name='Match Duration',
                                            hovertext=[f'Duration: {duration} minute'
                                                       for duration in match_duration['Duration']]
                                            ))
    fig_match_duration.update_layout(title=dict(text='Match Duration Over Time', x=0.5, y=0.95), xaxis_title='Year',
                                     yaxis_title='Match Duration (minutes)')

    return render_template('displayStat.html', plot_win_loss=fig_win_loss.to_html(full_html=False),
                           plot_points_scored=fig_points_scored.to_html(full_html=False),
                           plot_match_duration=fig_match_duration.to_html(full_html=False))


if __name__ == '__main__':
    app.run(debug=True)
