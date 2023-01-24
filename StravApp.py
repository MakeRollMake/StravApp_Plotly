from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px

FA = "https://use.fontawesome.com/releases/v5.12.1/css/all.css"

app = Dash(external_stylesheets=[dbc.themes.SLATE, FA])

# Iris bar figure
def drawFigure():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=px.bar(
                        df, x="sepal_width", y="sepal_length", color="species"
                    ).update_layout(
                        template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
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
df = px.data.iris()


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
                dbc.Button("Github Repository", href='https://github.com/MakeRollMake/Dash_test_render', className="me-1"),
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
                    drawText(8986, 'Total bike distance (KM)')
                ], width=4),
                dbc.Col([
                    drawText(2567, 'Total run distance (KM)')
                ], width=4),
                dbc.Col([
                    drawText(3, 'Total swim distance (KM)')
                ], width=4)
            ], align='center'),

            html.Br(),

            dbc.Row([
                dbc.Col([
                    drawText(456, 'Bike activities counter')
                ], width=4),
                dbc.Col([
                    drawText(318, 'Run activities counter')
                ], width=4),
                dbc.Col([
                    drawText(1, 'Swim activities counter')
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
    ),

    dbc.Card(
        dbc.CardBody([
            html.H4("Last activity", className="display-3"),
            dbc.Row([
                dbc.Col([
                    drawText(8986, 'Total bike distance (KM)')
                ], width=4),
                dbc.Col([
                    drawText(2567, 'Total run distance (KM)')
                ], width=4),
                dbc.Col([
                    drawText(3, 'Total swim distance (KM)')
                ], width=4)
            ], align='center'),

            html.Br(),

            dbc.Row([
                dbc.Col([
                    drawText(456, 'Bike activities counter')
                ], width=4),
                dbc.Col([
                    drawText(318, 'Run activities counter')
                ], width=4),
                dbc.Col([
                    drawText(1, 'Swim activities counter')
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
