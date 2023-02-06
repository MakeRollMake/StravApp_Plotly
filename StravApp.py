from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from plotly_calplot import calplot

FA = "https://use.fontawesome.com/releases/v5.12.1/css/all.css"
app = Dash(external_stylesheets=[dbc.themes.SLATE, FA])

# ----------ColorPalettes--------- #
# https://coolors.co/palette/001219-005f73-0a9396-94d2bd-e9d8a6-ee9b00-ca6702-bb3e03-ae2012-9b2226
color1 = '#001219'
color2 = color_ride = '#005f73'
color3 = '#0a9396'
color4 = color_kayaking = '#94d2bd'
color5 = '#e9d8a6'
color6 = color_run = '#ee9b00'
color7 = '#ca6702'
color8 = color_iceskate = '#bb3e03'
color9 = '#ae2012'
color10 = color_swim = '#9b2226'


# Iris bar figure
def drawFigure():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=px.bar(
                        df_demo, x="sepal_width", y="sepal_length", color="species"
                    ).update_layout(
                        template='plotly_dark',
                        plot_bgcolor='rgba(0, 0, 0, 0)',
                        paper_bgcolor='rgba(0, 0, 0, 0)',
                    ),
                    config={
                        'displayModeBar': False
                    }
                )
            ])
        ),
    ])


# Text field
def drawText(kpi, kpi_info):
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2(kpi),
                    html.H6(kpi_info),
                ], style={'textAlign': 'center'})
            ])
        ),
    ])


# Data
df_demo = px.data.iris()

# Create the dataframe
df = pd.read_csv('Data/activities_clean.csv')
df_map = pd.read_csv('Data/activities_clean_map.csv')
# converts the 'start_date' column to datetime format
df['start_date'] = pd.to_datetime(df['start_date'])

# ---------- OVERALL DATA ---------- #
# KPIs 1: BIKE
total_bike_distance = round(df[(df['type'] == 'Ride')]['distance'].sum() / 1000)
bike_count = len(df[df['type'] == 'Ride'])
bike_time = round(df[(df['type'] == 'Ride')]['moving_time'].sum() / 3600)
# KPIs 2: RUN
total_run_distance = round(df[(df['type'] == 'Run')]['distance'].sum() / 1000)
run_count = len(df[df['type'] == 'Run'])
run_time = round(df[(df['type'] == 'Run')]['moving_time'].sum() / 3600)
# KPIs 3: SWIM
# add of 4km and 2H because I clearly don't swim enough :/
total_swim_distance = round((df[(df['type'] == 'Swim')]['distance'].sum() / 1000) + 4)
swim_count = len(df[df['type'] == 'Swim'])
swim_time = round((df[(df['type'] == 'Swim')]['moving_time'].sum() / 3600) + 2)

# create fig1: Strava activities average speed (km/h)
fig1 = px.scatter(
    df, x='start_date', y='average_speed', color='type',
    title='Activities average speed (km/h), a third dimension (distance) is shown through size of markers',
    size='distance',
    labels={
        "type": "Activity type",
        "start_date": "Start Date",
        "average_speed": "Average Speed (km/h)"
    },
    color_discrete_map={'Ride': color_ride,
                        'Run': color_run,
                        'Kayaking': color_kayaking,
                        'IceSkate': color_iceskate,
                        'Swim': color_swim}
    )
fig1.update_layout(template='plotly_dark',
                   plot_bgcolor='rgba(0, 0, 0, 0)',
                   paper_bgcolor='rgba(0, 0, 0, 0)', )
# create fig3: calendar heatmap daily activities number
# Create the df_cal dataframe with the start_date and counts column from df_demo values
df_cal = df['start_date'].value_counts().rename_axis('start_date').reset_index(name='counts')
# Sort the dataframe by the 'start_date' column in ascending order and update the dataframe in place
df_cal.sort_values(by='start_date', inplace=True)
# calendar heatmap
fig3 = calplot(df_cal, x="start_date", y="counts", years_title=True, colorscale="blues", gap=4)
fig3.update_layout(template='plotly_dark',
                   plot_bgcolor='rgba(0, 0, 0, 0)',
                   paper_bgcolor='rgba(0, 0, 0, 0)', )
# create fig4: pie chart moving time by activities type
fig4 = px.pie(df, values='moving_time', names='type', color='type',
              title='Activities Type Moving Time',
              color_discrete_map={'Ride': color_ride,
                                  'Run': color_run,
                                  'Kayaking': color_kayaking,
                                  'IceSkate': color_iceskate,
                                  'Swim': color_swim})
fig4.update_traces(textposition='inside', textinfo='percent+label')
fig4.update_layout(template='plotly_dark',
                   plot_bgcolor='rgba(0, 0, 0, 0)',
                   paper_bgcolor='rgba(0, 0, 0, 0)', )

# create fig5: pie chart distance by activities type
fig5 = px.pie(df, values='distance', names='type', color='type',
              title='Activities Type Distance',
              color_discrete_map={'Ride': color_ride,
                                  'Run': color_run,
                                  'Kayaking': color_kayaking,
                                  'IceSkate': color_iceskate,
                                  'Swim': color_swim})
fig5.update_traces(textposition='inside', textinfo='percent+label')
fig5.update_layout(template='plotly_dark',
                   plot_bgcolor='rgba(0, 0, 0, 0)',
                   paper_bgcolor='rgba(0, 0, 0, 0)', )
# create fig6: moving time cumulative sum
df['moving_time_cumsum_bike'] = df[df['type'] == 'Ride'].loc[::-1, 'moving_time'].cumsum()[::-1]/1000
df['moving_time_cumsum_run'] = df[df['type'] == 'Run'].loc[::-1, 'moving_time'].cumsum()[::-1]/1000
# df['moving_time_cumsum_kayaking'] = df[df['type'] == 'Kayaking'].loc[::-1, 'moving_time'].cumsum()[::-1]/1000
# df['moving_time_cumsum_IceSkate'] = df[df['type'] == 'IceSkate'].loc[::-1, 'moving_time'].cumsum()[::-1]/1000
# df['moving_time_cumsum_Swim'] = df[df['type'] == 'Swim'].loc[::-1, 'moving_time'].cumsum()[::-1]/1000
fig6 = px.line(df, x='start_date',
               y=['moving_time_cumsum_bike', 'moving_time_cumsum_run'],
               title='Moving Time Cumulative Sum',
               labels={"variable": "Activity type",
                       "start_date": "Start Date",
                       "value": "Moving time"
                       },
               color_discrete_map={"moving_time_cumsum_bike": color_ride,
                                   "moving_time_cumsum_run": color_run
                                   }
               )
fig6.update_traces(connectgaps=True)
fig6.update_layout(template='plotly_dark',
                   plot_bgcolor='rgba(0, 0, 0, 0)',
                   paper_bgcolor='rgba(0, 0, 0, 0)', )

# ---------- LAST ACTIVITY ---------- #
# KPIS
last_name = df['name'][0]
last_start_date = df['start_date'][0].date()
last_start_time = df['start_time'][0]
last_type = df['type'][0]
last_distance = df['distance'][0]
last_average_speed = df['average_speed'][0]
last_elev_high = df['elev_high'][0]

# ---------- OVERALL DATA TAB---------- #
overall_data_tab = dbc.Card(
    dbc.CardBody([
        html.H4("Overall Data", className="display-3"),
        dbc.Row([
            dbc.Col([
                drawText(total_bike_distance, 'Total bike distance (KM)')
            ], width=4),
            dbc.Col([
                drawText(total_run_distance, 'Total run distance (KM)')
            ], width=4),
            dbc.Col([
                drawText(total_swim_distance, 'Total swim distance (KM)')
            ], width=4)
        ], align='center'),

        html.Br(),

        dbc.Row([
            dbc.Col([
                drawText(bike_time, 'Total bike time (H)')
            ], width=4),
            dbc.Col([
                drawText(run_time, 'Total run time (H)')
            ], width=4),
            dbc.Col([
                drawText(swim_time, 'Total swim time (H)')
            ], width=4)
        ], align='center'),

        html.Br(),

        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(id='graph4', figure=fig4)
                    )
                )
            ], width=3),
            dbc.Col([
                dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(id='graph5', figure=fig5)
                    )
                )
            ], width=3),
            dbc.Col([
                dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(id='graph6', figure=fig6)
                    )
                )
            ], width=6),
        ], align='center'),

        html.Br(),

        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(id='graph3', figure=fig3)
                    )
                )
            ], width=12),
        ], align='center'),

        html.Br(),

        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody(
                        dcc.Graph(id='graph1', figure=fig1)
                    )
                )
            ], width=12)
        ], align='center'),
    ]), color='dark'
)

# ---------- LAST ACTIVITY TAB---------- #
last_activity_tab = dbc.Card(
    dbc.CardBody([
        html.H4("Last activity", className="display-3"),
        dbc.Row([
            dbc.Col([
                drawText(last_name, 'Name')
            ], width=4),
            dbc.Col([
                drawText(last_start_date, 'Date (yyyy-mm-dd)'),
                drawText(last_start_time, 'Time (hh:mm:ss)'),
            ], width=4),
            dbc.Col([
                drawText(last_type, 'Type')
            ], width=4)
        ], align='center'),

        html.Br(),

        dbc.Row([
            dbc.Col([
                drawText(last_distance, 'Distance (m)')
            ], width=4),
            dbc.Col([
                drawText(last_average_speed, 'Average speed')
            ], width=4),
            dbc.Col([
                drawText(last_elev_high, 'Positive elevation')
            ], width=4)
        ], align='center'),

        html.Br(),

        dbc.Row([
            dbc.Col([
                drawFigure()
            ], width=3),
            dbc.Col([
                drawFigure()
            ], width=3),
            dbc.Col([
                drawFigure()
            ], width=6),
        ], align='center'),

        html.Br(),

        dbc.Row([
            dbc.Col([
                drawFigure()
            ], width=9),
            dbc.Col([
                drawFigure()
            ], width=3),
        ], align='center'),
    ]), color='dark'
)

monthly_data_tab = "TODO"

weekly_data_tab = "TODO"

progress_tab = dbc.Card(
    dbc.CardBody(
        [
            html.P("You are the GOAT !!", className="card-text")
        ]
    ),
    className="mt-3"
)

tabs = dbc.Tabs(
    [
        dbc.Tab(overall_data_tab, label="Overall Data"),
        dbc.Tab(last_activity_tab, label="Last Activity"),
        dbc.Tab(monthly_data_tab, label="Monthly Data", disabled=True),
        dbc.Tab(weekly_data_tab, label="Weekly Data", disabled=True),
        dbc.Tab(progress_tab, label="Progress")
    ]
)

app.layout = html.Div([
    dbc.Card(
        dbc.CardBody([
            dbc.Container(
                [
                    html.H1("STRAVA DATA VISUALIZATION", className="display-3"),
                    html.P(
                        "Use of Dash & Plotly to visualize Strava Activity Data.",
                        className="lead",
                    ),
                    html.Hr(className="my-2"),
                    html.P([
                        dbc.Button("Github Repository", href='https://github.com/MakeRollMake/StravApp_Plotly.git',
                                   className="me-1"),
                        dbc.Button("Getting Started with the Strava API",
                                   href='https://developers.strava.com/docs/getting-started/', className="me-1"),
                        dbc.Button("WIP Strava Jupyter Notebook",
                                   href='https://github.com/MakeRollMake/Dash_test_render/blob/main/WIP%20Strava%20Jupyter%20Notebook.ipynb',
                                   className="me-1")
                    ])
                ],
                fluid=True,
                className="h-100 p-5 text-light bg-dark rounded-3"

            ),
            tabs
        ])
    )
])

# Run app
if __name__ == '__main__':
    #app.run_server(debug=True)
    app.run_server(host='0.0.0.0', debug=True)
