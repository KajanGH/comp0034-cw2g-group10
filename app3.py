import pydeck as pdk
import pandas as pd  # Import pandas for DataFrame manipulation

# Load data from URL
UK_ACCIDENTS_DATA = 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/3d-heatmap/heatmap-data.csv'
POP_DATA_URL = 'https://raw.githubusercontent.com/KajanGH/data/main/prepared_ctry.csv'

# Load population data into a DataFrame
#pop_data = pd.read_json(POP_DATA_URL)

# Define the layer
layer = pdk.Layer(
    'HexagonLayer',  # `type` positional argument is here
    POP_DATA_URL,
    opacity=0.8,
    stroked=False,
    filled=True,
    extruded=True,
    wireframe=True,
    get_elevation='age_0',
    get_fill_color='[255, 255, 0]',
    get_line_color=[255, 255, 255],
    pickable=True)

# Set the viewport location
view_state = pdk.ViewState(
    longitude=-1.415,
    latitude=52.2323,
    zoom=6,
    min_zoom=5,
    max_zoom=15,
    pitch=40.5,
    bearing=-27.36
)

# Combine all elements and render a viewport
r = pdk.Deck(layers=[layer], initial_view_state=view_state)
r.to_html('test3.html')
