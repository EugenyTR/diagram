import dash
import dash.dcc as dcc
import dash.html as html
import dash.dash_table as dash_table
import plotly.express as px
import pandas as pd
import io
import base64
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Генератор инфографики из Excel"),
    dcc.Upload(
        id='upload-data',
        children=html.Button('Загрузить Excel-файл'),
        multiple=False
    ),
    html.Div(id='output-data-upload'),
    dcc.Dropdown(id='chart-type', options=[
        {'label': 'Столбчатая диаграмма', 'value': 'bar'},
        {'label': 'Круговая диаграмма', 'value': 'pie'},
        {'label': 'Линейная диаграмма', 'value': 'line'},
        {'label': 'Диаграмма рассеяния', 'value': 'scatter'}
    ], placeholder="Выберите тип диаграммы"),
    dcc.Graph(id='graph-output')
])

def parse_contents(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_excel(io.BytesIO(decoded))
    return df

@app.callback(
    [Output('output-data-upload', 'children'), Output('graph-output', 'figure')],
    [Input('upload-data', 'contents'), Input('chart-type', 'value')]
)
def update_output(contents, chart_type):
    if not contents:
        return html.Div(), {}
    
    df = parse_contents(contents)
    table = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records')
    )

    if not chart_type:
        return table, {}

    if chart_type == 'bar':
        fig = px.bar(df, x=df.columns[0], y=df.columns[1])
    elif chart_type == 'pie':
        fig = px.pie(df, names=df.columns[0], values=df.columns[1])
    elif chart_type == 'line':
        fig = px.line(df, x=df.columns[0], y=df.columns[1])
    elif chart_type == 'scatter':
        fig = px.scatter(df, x=df.columns[0], y=df.columns[1])
    else:
        fig = {}

    return table, fig

if __name__ == '__main__':
    app.run(debug=True)
