import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Verileri CSV dosyasından yükle
url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
df = pd.read_csv(url)

# Ülkeler listesi
countries = df['location'].unique()

# Dash uygulamasını oluştur
app = dash.Dash(__name__)
server = app.server

# Uygulama düzeni
app.layout = html.Div([
    html.H1("Dünya Çapında COVID-19 Vakaları Haritası ve Ülke Verileri"),
    dcc.Graph(id='world-map'),
    
    html.Label("Vaka Sayısı Tipi:"),
    dcc.Dropdown(
        id='case-type-dropdown',
        options=[
            {'label': 'Toplam Vaka Sayısı', 'value': 'total_cases'},
            {'label': 'Toplam Ölüm Sayısı', 'value': 'total_deaths'},
            {'label': 'Toplam İyileşen Sayısı', 'value': 'total_recovered'},
        ],
        value='total_cases',
        clearable=False
    ),

    html.Label("Ülkeleri Seçin:"),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in countries],
        value=['Turkey', 'Germany'],  # Varsayılan olarak seçili ülkeler
        multi=True
    ),

    dcc.Graph(id='pie-chart')
])

# Callback fonksiyonu - Dünya Haritası
@app.callback(
    Output('world-map', 'figure'),
    [Input('case-type-dropdown', 'value')]
)
def update_map(case_type):
    fig = px.choropleth(
        df,
        locations='iso_code',
        color=case_type,
        hover_name='location',
        animation_frame='date',
        projection='natural earth',
        color_continuous_scale='Viridis',
        title=f"Dünya Genelinde COVID-19 {case_type.capitalize()} Haritası",
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=30, b=0),
        coloraxis_colorbar=dict(title=case_type.capitalize())
    )
    return fig

# Callback fonksiyonu - Daire Dilimli Grafik
@app.callback(
    Output('pie-chart', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('case-type-dropdown', 'value')]
)
def update_pie_chart(selected_countries, case_type):
    filtered_df = df[df['location'].isin(selected_countries)]
    total_values = filtered_df.groupby('location')[case_type].max().reset_index()

    fig = px.pie(
        total_values,
        values=case_type,
        names='location',
        title=f"{', '.join(selected_countries)} Ülkelerinde COVID-19 {case_type.capitalize()} Dağılımı",
        labels={'location': 'Ülke'}
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)


with open("dash_uygulamasi.html", "w") as file:
    file.write(app.layout.to_html())
