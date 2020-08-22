#import modul

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

data_canada = px.data.gapminder().query("country == 'Canada'")

fig = px.bar(data_canada, x='year', y='pop')

#inisialisasi
app = dash.Dash()

#layout

app.layout = html.Div([
    html.H1("Hi!", style={'text-align':'center', 'color':'red'}),
    html.Div("Selamat Datang di Techtalk HammerCode"),
    html.Br(),
    html.Div(["Masukkan Nama: ",
              dcc.Input(id='my-input', value='Ashari', type='text')]),
    html.Br(),
    html.Div(id="my-output"),
    dcc.Graph(figure=fig)
])

@app.callback(
    Output(component_id='my-output', component_property='children'),
    [Input(component_id='my-input', component_property='value')]
)
def update_output_div(input_value):
    return 'Semangat belajar koding: {}'.format(input_value)

if __name__ == '__main__':
    app.run_server(port=4050, debug=True)