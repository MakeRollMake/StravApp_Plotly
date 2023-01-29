from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from plotly_calplot import calplot


FA = "https://use.fontawesome.com/releases/v5.12.1/css/all.css"
app = Dash(external_stylesheets=[dbc.themes.SLATE, FA])

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

# create the dataframe
df = pd.read_csv('Data/activities_clean.csv')
df_map = pd.read_csv('Data/activities_clean_map.csv')
# converts the 'start_date' column to datetime format
df['start_date'] = pd.to_datetime(df['start_date'])


# ---------- OVERALL DATA ---------- #
# KPIs 1: BIKE
total_bike_distance = round(df[(df['type'] == 'Ride')]['distance'].sum()/1000)
bike_count = len(df[df['type'] == 'Ride'])
bike_time = round(df[(df['type'] == 'Ride')]['moving_time'].sum()/3600)
# KPIs 2: RUN
total_run_distance = round(df[(df['type'] == 'Run')]['distance'].sum()/1000)
run_count = len(df[df['type'] == 'Run'])
run_time = round(df[(df['type'] == 'Run')]['moving_time'].sum()/3600)
# KPIs 3: SWIM
# add of 4km and 2H because I clearly don't swim enough :/
total_swim_distance = round((df[(df['type'] == 'Swim')]['distance'].sum()/1000) + 4)
swim_count = len(df[df['type'] == 'Swim'])
swim_time = round((df[(df['type'] == 'Swim')]['moving_time'].sum()/3600) + 2)

# create fig1: Strava activities average speed (km/h)
fig1 = px.scatter(
    df, x='start_date', y='average_speed', color='type',
    title='Activities average speed (km/h), a third dimension (distance) is shown through size of markers',
    size='distance',
    labels={
        "type": "Activity type",
        "start_date": "Start Date",
        "average_speed": "Average Speed (km/h)"
    })
fig1.update_layout(template='plotly_dark',
                   plot_bgcolor='rgba(0, 0, 0, 0)',
                   paper_bgcolor='rgba(0, 0, 0, 0)',)
# create fig3: calendar heatmap daily activities number
# Create the df_cal dataframe with the start_date and counts column from df_demo values
df_cal = df['start_date'].value_counts().rename_axis('start_date').reset_index(name='counts')
# Sort the dataframe by the 'start_date' column in ascending order and update the dataframe in place
df_cal.sort_values(by='start_date', inplace=True)
# calendar heatmap
fig3 = calplot(df_cal, x="start_date", y="counts", years_title=True, colorscale="blues", gap=4)
fig3.update_layout(template='plotly_dark',
                   plot_bgcolor='rgba(0, 0, 0, 0)',
                   paper_bgcolor='rgba(0, 0, 0, 0)',)


# ---------- LAST ACTIVITY ---------- #
# KPIS
last_name = df['name'][0]
last_start_date = df['start_date'][0].date()
last_start_time = df['start_time'][0]
last_type = df['type'][0]
last_distance = df['distance'][0]
last_average_speed = df['average_speed'][0]
last_elev_high = df['elev_high'][0]


# ---------- APP LAYOUT ---------- #
app.layout = html.Div([
    dbc.Container(
        [
            html.H1("STRAVA DATA VISUALIZATION", className="display-3"),
            html.P(
                "Use of Dash & Plotly to visualize Strava Activity Data.",
                className="lead",
            ),
            html.Hr(className="my-2"),
            html.P([
                dbc.Button("Github Repository", href='https://github.com/MakeRollMake/StravApp_Plotly.git', className="me-1"),
                dbc.Button("Getting Started with the Strava API", href='https://developers.strava.com/docs/getting-started/', className="me-1"),
                dbc.Button("WIP Strava Jupyter Notebook", href='https://github.com/MakeRollMake/Dash_test_render/blob/main/WIP%20Strava%20Jupyter%20Notebook.ipynb', className="me-1")
            ])
        ],
        fluid=True,
        className="h-100 p-5 text-light bg-dark rounded-3"

    ),

    dbc.Card(
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
                    drawFigure()
                ], width=3),
                dbc.Col([
                    drawFigure()
                ], width=3),
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody(
                            dcc.Graph(id='graph2', figure=fig1)
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
                            dcc.Graph(id='graph2', figure=fig1)
                        )
                    )
                ], width=9),
                dbc.Col([
                    drawFigure()
                ], width=3),
            ], align='center'),
        ]), color='dark'
    ),

    dbc.Card(
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
])

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
