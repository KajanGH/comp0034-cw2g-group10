import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)

# Load data
data_url = 'https://media.githubusercontent.com/media/KajanGH/data/main/prepared_lad.csv'
data = pd.read_csv(data_url)

@app.route('/map2')
def map2():
    # Perform data analysis and calculations
    start_age = 0
    end_age = 95



    def calculate_elevation_in_range(row):
        return sum(row[f'age_{i}'] if f'age_{i}' in row else 0 for i in range(start_age, end_age + 1))
    
    def interpolate_colour_r(elevation):
        # Normalize elevation between 0 and 1
        normalized_elevation = (elevation - min_elevation) / (max_elevation - min_elevation)
        
        # Define color values for green, yellow, orange, and red
        green = [0, 255, 0]  # Green
        yellow = [255, 255, 0]  # Yellow
        orange = [255, 165, 0]  # Orange
        red = [255, 0, 0]  # Red
        
        # Interpolate color based on elevation
        if normalized_elevation < 0.5:
            # Interpolate between green and yellow
            color = [int((1 - 2 * normalized_elevation) * green[i] + 2 * normalized_elevation * yellow[i]) for i in range(3)]
        else:
            # Interpolate between yellow and red
            color = [int((1 - 2 * (normalized_elevation - 0.5)) * orange[i] + 2 * (normalized_elevation - 0.5) * red[i]) for i in range(3)]
        
        return color[0] 

    def interpolate_colour_g(elevation):
        # Normalize elevation between 0 and 1
        normalized_elevation = (elevation - min_elevation) / (max_elevation - min_elevation)
        
        # Define color values for green, yellow, orange, and red
        green = [0, 255, 0]  # Green
        yellow = [255, 255, 0]  # Yellow
        orange = [255, 165, 0]  # Orange
        red = [255, 0, 0]  # Red
        
        # Interpolate color based on elevation
        if normalized_elevation < 0.5:
            # Interpolate between green and yellow
            color = [int((1 - 2 * normalized_elevation) * green[i] + 2 * normalized_elevation * yellow[i]) for i in range(3)]
        else:
            # Interpolate between yellow and red
            color = [int((1 - 2 * (normalized_elevation - 0.5)) * orange[i] + 2 * (normalized_elevation - 0.5) * red[i]) for i in range(3)]
        
        return color[1]
    

    fdata = data[data['sex'] == 'female']
    #fdata = fdata[fdata['Region'] == 'London']
    fdata = fdata[fdata['ITL'] == fdata['ITL']]
    fdata = fdata[fdata['extract_date'] == '2014-10-01']
    #fdata = fdata[fdata['LAD'] != 'City of London']
    fdata['elevation'] = fdata.apply(calculate_elevation_in_range, axis=1)
    max_elevation = fdata['elevation'].max()
    min_elevation = fdata['elevation'].min()
    scale = 40000 / max_elevation
    fdata['red'] = fdata['elevation'].apply(interpolate_colour_r)
    fdata['green'] = fdata['elevation'].apply(interpolate_colour_g)
    
    # Pass processed data to template
    return render_template('MAP2.html', data=fdata.to_dict(orient='records'), start_age=start_age, end_age=end_age, max_elevation=max_elevation, min_elevation=min_elevation, scale=scale)

if __name__ == '__main__':
    app.run(debug=True)
