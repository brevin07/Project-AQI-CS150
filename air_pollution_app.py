import pandas as pd
import plotly.express as px

from dash import Dash, dcc, html, Input, Output

__author__ = "Brevin Tating"
__credits__ = ["Brevin Tating"]
__email__ = "btating@westmont.edu"

df_2016 = pd.read_csv('all_cities_2016.csv')
df_2017 = pd.read_csv('all_cities_2017.csv')
df_2018 = pd.read_csv('all_cities_2018.csv')
df_2019 = pd.read_csv('all_cities_2019.csv')
df_2020 = pd.read_csv('all_cities_2020.csv')
df_2021 = pd.read_csv('all_cities_2021.csv')
df_2022 = pd.read_csv('all_cities_2022.csv')


df_2016["Date"] = pd.to_datetime(df_2016["Date"])
df_2017["Date"] = pd.to_datetime(df_2017["Date"])
df_2018["Date"] = pd.to_datetime(df_2018["Date"])
df_2019["Date"] = pd.to_datetime(df_2019["Date"])
df_2020["Date"] = pd.to_datetime(df_2020["Date"])
df_2021["Date"] = pd.to_datetime(df_2021["Date"])
df_2022["Date"] = pd.to_datetime(df_2022["Date"])

stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = Dash(__name__, external_stylesheets=stylesheets)

df_dict = {
    '2016': df_2016,
    '2017': df_2017,
    '2018': df_2018,
    '2019': df_2019,
    '2020': df_2020,
    '2021': df_2021,
    '2022': df_2022
}

app.layout = html.Div(
    [
        html.Div(
            html.H2(
                "Air Pollution Analysis of Northern California Cities by Year", style={"textAlign": "center"}
            ),
            className="row"
        ),
        html.Div(dcc.Graph(id="air-graph", figure={}), className="row"),

        html.Div([
            dcc.Slider(2016, 2022, 1, value = 2016, id="year-slider"),
            html.Div(id="slider-output-container"
            ),
            html.Div(
                dcc.Dropdown(
                    id="air-dropdown",
                    multi=True,
                    options=[
                        {"label": x, "value": x} for x in sorted(df_2018["Local Site Name"].unique())
                    ],
                    value=[]
                ),
                className="three columns"
            ),
            html.Div(
                html.A(
                    id="data_link",
                    children="Data set used for analysis",
                    href= "https://www.epa.gov/outdoor-air-quality-data/download-daily-data"

                ),
                className="two columns"
            )
        ],
            className="row"

        )

    ]
)

# Callbacks *******************************************************************
@app.callback(
    Output(component_id="air-graph", component_property="figure"),
    [Input(component_id="year-slider", component_property="value"),
     Input(component_id="air-dropdown", component_property="value")]
)
def update_graph(year, cities_data):
    print(f"Year chosen by user: {year}")
    print(f"Cities chosen by user: {cities_data}")
    df_filtered = df_dict.get(year)

    if df_filtered is None:
        return {}

    if cities_data:
        df_filtered = df_filtered[df_filtered["Local Site Name"].isin(cities_data)]

    fig = px.line(
        data_frame=df_filtered,
        x="Date",
        y="Daily AQI Value",
        color="Local Site Name",
        log_y=True,
        labels={
            "Daily AQI Value": "Daily AQI Value",
            "Date": "Date",
            "Local Site Name": "Local Site Name"
        }
    )


    return fig



if __name__ == "__main__":
    app.run_server(debug=True)