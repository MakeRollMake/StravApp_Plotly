from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
from plotly_calplot import calplot
import dash_daq as daq

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)


# create the dataframe
df = pd.read_csv('activities_clean.csv')

# converts the 'start_date' column to datetime format
df['start_date'] = pd.to_datetime(df['start_date'])

# create fig1: strava activities distance (m)
fig1 = px.scatter(df, x='start_date', y='distance', color='type', title='Strava activities distance (m)',
                  labels={
                      "type": "Activity type",
                      "start_date": "Start Date",
                      "distance": "Distance (m)"
                  },
                  )
fig1.update_xaxes(rangeslider_visible=True,
                  rangeselector=dict(
                        buttons=list([
                            dict(count=1, label="1m", step="month", stepmode="backward"),
                            dict(count=6, label="6m", step="month", stepmode="backward"),
                            dict(count=1, label="YTD", step="year", stepmode="todate"),
                            dict(count=1, label="1y", step="year", stepmode="backward"),
                            dict(step="all")
                        ])
                  )
                  )

# create fig2: Strava activities average speed (km/h)
fig2 = px.scatter(df, x='start_date', y='average_speed', color='type', title='Strava activities average speed (km/h)', size='distance',
                  labels={
                      "type": "Activity type",
                      "start_date": "Start Date",
                      "average_speed": "Average Speed (km/h)"
                  },
                  )
fig2.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)

# create fig3: calendar heatmap daily activities number
# Create the df_cal dataframe with the start_date and counts column from df values
df_cal = df['start_date'].value_counts().rename_axis('start_date').reset_index(name='counts')
# Sort the dataframe by the 'start_date' column in ascending order and update the dataframe in place
df_cal.sort_values(by='start_date', inplace=True)
# calendar heatmap
fig3 = calplot(df_cal, x="start_date", y="counts", years_title=True, colorscale="blues", gap=4)


########### -This part is dedicated to the last activity analysis- ###########
# select the last activity
act_coord = eval(df['map.polyline'][0])
# create 2 lists for latitude and longitude values of the activity
act_latitude = []
act_longitude = []
i = 0
while i < len(act_coord):
    act_latitude.append(act_coord[i][0])
    act_longitude.append(act_coord[i][1])
    i += 1
# creates df for latitude and longitude values
df_act_coord = pd.DataFrame()
df_act_coord['latitude'] = act_latitude
df_act_coord['longitude'] = act_longitude

# create fig4: map with the last activity
mid_point = round(len(df_act_coord)/2)
fig4 = px.line_mapbox(df_act_coord, lat="latitude", lon="longitude")
fig4.update_layout(
    mapbox_style="open-street-map", mapbox_zoom=12,
    #mapbox_center_lat=df_act_coord['latitude'][mid_point],
    #mapbox_center_lon=df_act_coord['longitude'][mid_point],
    margin={"r": 10, "t": 10, "l": 10, "b": 10},
    width=800, height=800
)
fig4.update_traces(line=dict(width=6))


markdown_text = '''
#### Using Dash/Plotly to visualize Strava Activity Data.

This Dashboard is linked to the following [Github Repository](https://github.com/MakeRollMake/Dash_test_render).

To download your data from strava, here is a brief overview on how to use strava API: [Getting Started with the Strava API](https://developers.strava.com/docs/getting-started/).

Once you manage to get your access & refresh tokens, you can use this [WIP Strava Jupyter Notebook](https://github.com/MakeRollMake/Dash_test_render/blob/main/WIP%20Strava%20Jupyter%20Notebook.ipynb)
'''

# KPIs 1: BIKE
total_bike_distance = round(df[(df['type'] == 'Ride')]['distance'].sum()/1000)
bike_count = len(df[df['type'] == 'Ride'])

# KPIs 2: RUN
total_run_distance = round(df[(df['type'] == 'Run')]['distance'].sum()/1000)
run_count = len(df[df['type'] == 'Run'])

# KPIs 3: SWIM
# add of 2km because I clearly don't swim enough :/
total_swim_distance = round((df[(df['type'] == 'Swim')]['distance'].sum()/1000) + 2)
swim_count = len(df[df['type'] == 'Swim'])


green = '#68c3a3'
blue = '#0b7fab'

app.layout = html.Div(children=[
    html.Div([
        html.H1(children='STRAVA DATA VISUALIZATION', style={'textAlign': 'center', 'color': '#f46f06'}),
        dcc.Markdown(children=markdown_text, style={'margin': '15px'}),
    ]),

    html.Div(children=[
        daq.LEDDisplay(
            label="Bike distance (KM)", labelPosition='top', value=total_bike_distance,
            color=green,
            style={'width': '29%', 'display': 'inline-block', 'margin': '15px'}),
        daq.LEDDisplay(
            label="Run distance (KM)", labelPosition='top', value=total_run_distance,
            color=green,
            style={'width': '29%', 'display': 'inline-block', 'margin': '15px'}),
        daq.LEDDisplay(
            label="Swim distance (KM)", labelPosition='top', value=total_swim_distance,
            color=green,
            style={'width': '29%', 'display': 'inline-block', 'margin': '15px'})
    ]),

    html.Div(children=[
        daq.LEDDisplay(
            label="Bike Activities Counter", labelPosition='top', value=bike_count,
            color=blue,
            style={'width': '29%', 'display': 'inline-block', 'margin': '15px'}),
        daq.LEDDisplay(
            label="Run Activities Counter", labelPosition='top', value=run_count,
            color=blue,
            style={'width': '29%', 'display': 'inline-block', 'margin': '15px'}),
        daq.LEDDisplay(
            label="Swim Activities Counter", labelPosition='top', value=swim_count,
            color=blue,
            style={'width': '29%', 'display': 'inline-block', 'margin': '15px'})
    ]),

    html.Div([
        dcc.Graph(id='graph1', figure=fig1),
        dcc.Graph(id='graph2', figure=fig2),
        dcc.Graph(id='graph3', figure=fig3),
        dcc.Graph(id='graph4', figure=fig4)
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
