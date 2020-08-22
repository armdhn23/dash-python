#import modul
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import base64

#menambahkan gambar
image_filename = 'asset/kd.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

#data
label = ["github", "stackoverflow", "pypl", "tiobe"]
indeks = [0, 1 ,2 ,3]
github = pd.read_csv('data/github.csv')
github = github.filter(['Language', 'Percentage', 'Source'])
stackoverflow = pd.read_csv('data/stackoverflow.csv')
pypl = pd.read_csv('data/pypl.csv')
pypl = pypl.filter(['Language', 'Share', 'Source'])
tiobe = pd.read_csv('data/tiobe.csv')
tiobe = tiobe.filter(['Language', 'Rating', 'Source'])

#inisialisasi dash
app = dash.Dash(__name__, title="Techtalk", external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

#layout
app.layout = html.Div([
    dbc.Row([
        dbc.Col(html.H2("Dashboard Kerabat Data", style={'margin-top':25, 'margin-left':50}), md=9),
        dbc.Col(
            html.Img(
            src='data:image/png;base64,{}'.format(encoded_image.decode()), style={'margin-top':20}
            ),  md =3
        )
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col(dbc.Card([
            html.H2("Linux", className='card-title'),
            html.P("Most Loved Platform", className='card-text')
        ],
        body=True,
        color='light')),

        dbc.Col(dbc.Card([
            html.H2("Perl", className='card-title'),
            html.P("Highest Salaries Worldwide", className='card-text')
        ],
        body=True,
        color='dark',
        inverse=True)),
        
        dbc.Col(dbc.Card([
            html.H2("Redis", className='card-title'),
            html.P("Most Loved Databases", className='card-text')
        ],
        body=True,
        color='primary',
        inverse=True))
    ]),
    dbc.Form(
            dbc.FormGroup(
            [
                dbc.Label("Dropdown", html_for="dropdown", style={'margin-left':60, 'margin-top':20}),
                html.Br(),
                dcc.Dropdown(
                    id="dropdown",
                    options=[{"label": label[k], "value": label[k]} for k in indeks],
                    value = "pypl",
                    style={'height': '30px', 'width': '400px','margin-left':30, 'margin-top':20}
                ),
            ]
        )
    ),
    html.H1(id="judul", style={'text-align':'center'}),
    dcc.Graph(id="grafik_hbar", figure={})
])

#the callback
@app.callback(
    [Output(component_id="judul", component_property="children"),
     Output(component_id='grafik_hbar', component_property='figure')],
    [Input(component_id='dropdown', component_property='value')]
)
def update_figures(dropdown):
    if dropdown == "github":
        df1 = github
        judul = df1.Source[0]
    elif dropdown == "stackoverflow":
        df1 = stackoverflow
        judul = df1.Source[0]
    elif dropdown == "pypl":
        df1 = pypl 
        judul = df1.Source[0]
    else:
        df1 = tiobe
        judul = df1.Source[0]

    fig = go.Figure(go.Bar(
            x=df1.iloc[0:,1],
            y=df1.iloc[0:,0],
            orientation='h',
            text = df1.iloc[0:,1],
            textposition='outside',),
          go.Layout(
            yaxis=dict(
            autorange='reversed'
            )
        ))
    fig.update_layout(title=judul, title_x=0.5)
    fig.update_xaxes(title_text=df1.columns[1])
    fig.update_yaxes(title_text=df1.columns[0])
    return "Sumber: {}".format(dropdown), fig


if __name__ == '__main__':
    app.run_server(debug=True, port=4050)
