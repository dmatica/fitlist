import os
import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Initialize the Dash app
app = dash.Dash(__name__)#, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Directory to list
base_dir = '/Users/davindersandhu/PycharmProjects/Fitcheck/Data/'
workout = 'Elliptical'


# Function to get a list of folders in the directory
def list_folders(directory):
    folders = []
    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            #print(dir)
            if dir.startswith(workout) and os.path.exists(os.path.join(root, dir)+'/'+os.path.basename(dir)+'_tracks.csv'):
                folder_path = os.path.join(root, dir)
                folders.append(folder_path)
    folders.sort(reverse=True)
    return folders


# Function to read data files and generate graphs
def generate_graphs(folder):
    print(folder)
    exercise = os.path.basename(os.path.normpath(folder))
    print(exercise)
    if os.path.exists(folder + '/' + exercise + '_tracks.csv'):
        active_energy = pd.read_csv(folder + '/Active Energy.csv')
        heart_rate_file = folder + '/' + exercise + '_tracks.csv'
        df_heart_rate = pd.read_csv(heart_rate_file, parse_dates=['Date/Time'])

        # Get workout duration from heart rate file
        workout_start = pd.to_datetime(df_heart_rate['Date/Time'].iloc[0]).tz_localize('America/New_York')
        workout_end = pd.to_datetime(df_heart_rate['Date/Time'].iloc[-1]).tz_localize('America/New_York')
        time_delta = workout_end - workout_start

        # Get average heart rate for duration of workout
        avg_heart_rate = df_heart_rate['Avg (count/min)'].mean()

        # Get sum of active calories burned for duration of workout
        total_active_energy = active_energy['Active Energy (kcal)'].sum()

        condition = df_heart_rate['Track Description'] == 'NaT'
        df1 = df_heart_rate[condition]
        df2 = df_heart_rate[~condition]

        df_active_energy = pd.read_csv(folder + '/Active Energy.csv', parse_dates=['Date/Time'])

        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=False,
            vertical_spacing=0.1,
            subplot_titles=('', "Top 5 Tracks"),
            row_heights=[0.75, 0.25],
            specs=[[{"secondary_y": True}], [{"type": "table"}]]
        )

        fig.add_trace(go.Line(x=df_active_energy['Date/Time'], y=60 * df_active_energy['Active Energy (kcal)'],
                              name='Active Energy (kcal/min)', line=dict(color='blue'), opacity=0.25,
                              hoverinfo='skip'), row=1, col=1)

        fig.add_trace(go.Scatter(x=df2['Date/Time'], y=df2['Avg (count/min)'],
                                 name='Heart Rate (bpm)', mode='markers', marker_line_width=1,
                                 hovertext=df2['Track Description'],
                                 marker=dict(color=df2['Avg (count/min)'], colorscale='jet',
                                             cmin=80, cmax=180)), row=1, col=1, secondary_y=True)
        fig.add_trace(go.Scatter(x=df1['Date/Time'], y=df1['Avg (count/min)'],
                                 name='Heart Rate (bpm)', mode='markers', marker_line_width=1, fillcolor='black',
                                 hoverinfo='skip'), row=1, col=1, secondary_y=True)

        grouped_data = (df2.groupby('Track Description')['Avg (count/min)'].mean()).sort_values(ascending=False)
        top_5_tracks = grouped_data.sort_values(ascending=False).head(5)
        dfx = grouped_data.reset_index()
        dfx.columns = ['Track Description', 'Avg (count/min)']

        fig.add_trace(
            go.Table(
                header=dict(
                    values=dfx.columns,
                    font=dict(size=11),
                    #height=25,
                    align="left"
                ),
                cells=dict(
                    values=[dfx.head(5)[k].tolist() for k in dfx.columns[0:]],
                    font=dict(size=10),
                    height=20,
                    align="left")
            ), row=2, col=1
        )

        fig.update_layout(
            yaxis=dict(title='Active Energy (kcal/min)', range=[0, 20], side='right', griddash='dot'),
            yaxis2=dict(title='Heart Rate (bpm)', range=[50, 200], overlaying='y', side='left'),
            xaxis=dict(title='Time', tickformat='%H:%M'),
            title="<b>" + exercise + "</b><br><sub><b>Total energy: </b>"+str(f"{total_active_energy:.2f}")+" kcal&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Average heart rate: </b>"+str(f"{avg_heart_rate:.2f}")+" BPM&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Total workout time: </b>"+str(f"{(time_delta).total_seconds()/60:.0f}")+" minutes</sub>",
            title_x=0.5,
            showlegend=False,
            margin=dict(b=20, l=20, r=20),
            plot_bgcolor='darkgrey'
        )

        return dcc.Graph(figure=fig, style={'width': '100%', 'height': '100%'})


# Layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("FitList v0"), style={'width':'100vw'}),

    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='folder-dropdown',
                options=[{'label': os.path.basename(folder), 'value': folder} for folder in list_folders(base_dir)],
                placeholder="Select a folder",
                style={'margin-bottom': '0px','padding-bottom':'0px','width':'20vw'}
            ),
            html.Div(id='graphs-container', style={'height':'90vh','padding-top':'0px','margin-top':'0px'})
        ], width=12, style={'padding-left':'10'})
    ]),
],fluid=True, style={'padding': '0', 'margin': '0'})


# Callback to update the graphs based on selected folder
@app.callback(
    Output('graphs-container', 'children'),
    [Input('folder-dropdown', 'value')]
)
def update_graphs(selected_folder):
    if selected_folder:
        return generate_graphs(selected_folder)
    return []


# Run the app
if __name__ == '__main__':
    app.title = "FitList"
    app.run_server(debug=False)
