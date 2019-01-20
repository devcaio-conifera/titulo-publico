import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv('titulos_dash.csv')
#df = pd.read_hdf('tp_hdf', 'result')

app = dash.Dash()
server = app.server


# https://dash.plot.ly/dash-core-components/dropdown
# We need to construct a dictionary of dropdown values for the years
titulo_options = []
for titulo in df['titulo_data'].unique():
    titulo_options.append({'label':str(titulo),'value':titulo})

app.layout = html.Div([
    dcc.Graph(id='graph'),
    dcc.Dropdown(id='titulo-picker',options=titulo_options,value=df['titulo_data'].values[0])
])

@app.callback(Output('graph', 'figure'),
              [Input('titulo-picker', 'value')])
def update_figure(selected_titulo):
    filtered_df = df[df['titulo_data'] == selected_titulo]
    traces=[]
    traces.append( go.Scatter(
                        x=filtered_df['Data_Base'],
                        y=filtered_df['PU_Compra_Manha'],
                        text=filtered_df['PU_Compra_Manha'],
                        mode='markers',
                        opacity=0.7,
                        marker={'size': 5},
                        name=selected_titulo
                    ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'tempo'},
            yaxis={'title': 'Preco de Compra'},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()
