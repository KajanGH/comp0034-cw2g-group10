import pandas as pd
import matplotlib.pyplot as plt
import calendar
import secrets
from flask import Flask, render_template, request, session
from collections import deque
from helpers import encode_auth_token, token_required, trends_box
from pathlib import Path
from datetime import date
import math
import sys
import os

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


#PUT LOCATION CSV HERE--------------
ctry_data = pd.read_csv('Datasets/Edited_Forecasts/combined_forecast_ctry_sex_age_group.csv')
rgn_data = pd.read_csv('Datasets/Edited_Forecasts/combined_forecast_Region_sex_age_group.csv')
itl_data = pd.read_csv('Datasets/Edited_Forecasts/combined_forecast_ITL_sex_age_group.csv')
lad_data = pd.read_csv('Datasets/Edited_Forecasts/combined_forecast_LAD_sex_age_group.csv')
#-----------------------------------------


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/account')
@token_required
def account():
    return render_template('account-page.html')

search = deque(["","",""],maxlen=3)
snapshots = deque([0,1,2,3,4,5,6,7,8],maxlen=9)
@app.route('/analytics', methods=['GET', 'POST'])
#@token_required
def analytics():
    save = True
    snapshotdata = pd.read_csv('static\snapshot\snapshotdata.csv')
    if len(snapshotdata) == 10: snapshotdata = snapshotdata.drop(snapshotdata.index[0])
    form = ""
    if request.method == 'POST':
        df = pd.read_csv('dataset/prepared_itl.csv',  usecols=lambda col: 'age' in col or col in ['Region','ITL', 'extract_date', 'sex'])
        for index,row in df.iterrows():
            df.at[index, 'year'] = int(row['extract_date'].split('-')[0])
            df.at[index, 'month'] = calendar.month_name[int(row['extract_date'].split('-')[1])]
        if 'Region' in request.form.keys():
            df = df[df['Region'] == (request.form['Region'])]
            form += request.form['Region']
        if 'sex' in request.form.keys():
            df = df[df['sex'] == request.form['sex'].lower()]
            form += " " + request.form['sex']
        if 'low-age' in request.form.keys() and int(request.form['low-age'])>0: low_age = int(request.form['low-age'])
        else: low_age = 0
        if 'high-age' in request.form.keys() and int(request.form['high-age'])<95: high_age = int(request.form['high-age'])
        else: high_age = 95
        form += " " + str(low_age) + "-" + str(high_age)
        if 'month' in request.form.keys():
            df = df[df['month'] == request.form['month'].capitalize()]
            form += " in " + request.form['month']
        if 'year' in request.form.keys():
            df = df[df['extract_date'].str.contains(request.form['year'])]
            form += " " + request.form['year']
        df.to_excel('static/public/filtered_data.xlsx')

        age_cols_to_keep = [f'age_{i}' for i in range(low_age, high_age + 1)]
        df = df[['Region','ITL', 'sex', 'year', 'month'] + age_cols_to_keep]
        ####AGE AGAINST YEARS GRAPH####
        # Calculate sum of each age range row
        age_columns = [col for col in df.columns if col.startswith('age_')]
        df['total_age_sum'] = round(df[age_columns].sum(axis=1))

        # Group by year and calculate the sum of total_age_sum
        age_sum_by_year = df.groupby('year')['total_age_sum'].sum()

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.plot(age_sum_by_year.index, age_sum_by_year.values, marker='o', linestyle='-')
        plt.title('Total People Over Years')
        plt.xlabel('Year')
        plt.ylabel('Total Age Sum')
        plt.grid(True)
        plt.xticks(age_sum_by_year.index)
        for i, txt in enumerate(age_sum_by_year.values):
            plt.annotate(txt, (age_sum_by_year.index[i], age_sum_by_year.values[i]), textcoords="offset points", xytext=(0,10), ha='center')
        plt.tight_layout()
        plt.savefig('static/public/graph1.png')
        if save: 
            snapshotdata.at[snapshots[0],"form"] = form
            snapshotdata.at[snapshots[0],"date"] = date.today()
            if os.path.exists(f'static/snapshot/graph{snapshots[0]}.png'): os.remove(f'static/snapshot/graph{snapshots[0]}.png')
            plt.savefig(f'static/snapshot/graph{snapshots[0]}.png')
            snapshotdata.at[snapshots[0],"img"] = f'static/snapshot/graph{snapshots[0]}.png'
            snapshots.append(snapshots[0])
            

        ####AGE DISTRIBUTION GRAPH####
        sumdict = {}
        for col in age_columns:
            sumdict[col.split("_")[-1]]=(round(df[col].sum(axis=0)))

        # Plotting
        plt.figure(figsize=(10, 6))
        bars = plt.bar(sumdict.keys(), sumdict.values())
        plt.xlabel('Age')
        plt.ylabel('Total Number of People')
        plt.title('Total Number of People per Age')
        plt.tight_layout()
        for bar in bars:
            height = bar.get_height()
            plt.annotate('{}'.format(height),
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
        plt.savefig('static/public/graph2.png')
        if save:
            snapshotdata.at[snapshots[0],"form"] = form
            snapshotdata.at[snapshots[0],"date"] = date.today()
            if os.path.exists(f'static/snapshot/graph{snapshots[0]}.png'): os.remove(f'static/snapshot/graph{snapshots[0]}.png')
            plt.savefig(f'static/snapshot/graph{snapshots[0]}.png')
            snapshotdata.at[snapshots[0],"img"] = f'static/snapshot/graph{snapshots[0]}.png'
            snapshots.append(snapshots[0])

        ###SEX PIE CHART###
        sex_age_counts = df.groupby('sex')[age_columns].sum()

        # Calculate the total number of people per sex
        total_people_per_sex = sex_age_counts.sum(axis=1)

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.pie(total_people_per_sex, labels=total_people_per_sex.index, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 30})
        plt.title('Sex Makeup', fontsize=60)
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig('static/public/graph3.png')

        ###LOCATION PIE CHART###
        location_age_counts = df.groupby('ITL')[age_columns].sum()

        # Calculate the total number of people per sex
        total_people_per_location = location_age_counts.sum(axis=1)

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.pie(total_people_per_location, labels=total_people_per_location.index, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 30})
        plt.title('ITL Ratio',fontsize=60)
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig('static/public/graph4.png')

        ###MONTH PIE CHART###
        month_counts = df['month'].value_counts()
        # Plotting
        plt.figure(figsize=(10, 6))
        plt.pie(month_counts, labels=month_counts.index, autopct='%1.1f%%', startangle=140,textprops={'fontsize': 25})
        plt.title('Month Ratio',fontsize=60)
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig('static/public/graph5.png')

        search.append(form)

        if save: snapshotdata.to_csv('static\snapshot\snapshotdata.csv',index=False)
    return render_template('analytics-page.html',DataToRender = search )

@app.route('/snapshot')
#@token_required
def snapshot():
    snapshotdata = pd.read_csv('static\snapshot\snapshotdata.csv')
    return render_template('snapshot-page.html',dates = snapshotdata['date'].values, info = snapshotdata['form'].values, imgs=snapshotdata['img'].values)

@app.route('/dashboard')
@token_required
def dashboard():
    return render_template('dashboard-page.html')

@app.route('/log-in', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        df = pd.read_csv("dataset/users.csv")
        if request.form['email'] not in df['email'].values:
            return render_template('log-in-page.html', error="User not registered"), 409
        if request.form['password'] != df[df['email'] == request.form['email']]['password'].values[0]:
            return render_template('log-in-page.html', error="Incorrect password"), 409
        id = df[df['email'] == request.form['email']]['id'].values[0]
        session['token'] = encode_auth_token(int(id))
        return render_template('log-in-page.html',success="Logged in successfully"),200
    return render_template('log-in-page.html'),200

@app.route('/settings')
@token_required
def settings():
    return render_template('settings-page.html')

@app.route('/sign-up',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        df = pd.read_csv("dataset\\users.csv")
        if request.form['password'] != request.form['repeatpassword']:
            return render_template('sign-up-page.html', error="Passwords do not match"), 409
        if request.form['email'] in df['email'].values: 
            return render_template('sign-up-page.html', error="Email already exists"), 409
        line = len(df)
        for field in request.form.keys():
            df.at[line,field] = request.form[field]
        df.at[len(df)-1,'id'] = line
        df.to_csv("dataset\\users.csv",index=False)
        return render_template('sign-up-page.html', success="User registered successfully"), 200
    return render_template('sign-up-page.html'), 200

@app.route('/map', methods=['GET', 'POST'])
#@token_required
def map():
    # Perform data analysis and calculations
    start_age = 0
    end_age = 95
    selected_layer = 'rgn'
    sexChoice = 'persons'
    year = 2023
    remove_values = []
    message = 'None Hidden'
    radius = 1000
    datecorrection = ""

    if request.method == 'POST':
        if 'layer' in request.form.keys(): selected_layer = request.form.get('layer')
        if 'sex' in request.form.keys(): sexChoice = request.form.get('sex')
        if 'start_age' in request.form.keys() and request.form['start_age']: start_age = int(request.form.get('start_age'))
        if 'end_age' in request.form.keys() and request.form['end_age']: end_age = int(request.form.get('end_age'))
        if 'year' in request.form.keys() and request.form['year']:
            year = int(request.form.get('year'))
            month = int(request.form.get('year'))%12 + 1


        if 'remove' in request.form.keys() and request.form['remove']:
            remove_values = request.form.get('remove').split('/')
    # Update data based on the selected layer
    if selected_layer == 'lad':
        data = lad_data
        radius = 1000
    elif selected_layer == 'itl':
        data = itl_data
        radius = 1500
    elif selected_layer == 'rgn':
        data = rgn_data
        radius = 3000
    else:
        # Handle invalid selection
        data = rgn_data
  
    if 'year' in request.form.keys():
        if month < 10: formatted_date = f'{math.floor(year/12)}-0{month}-01'
        else: formatted_date = f'{math.floor(year/12)}-{month}-01'
    else:
        formatted_date = '2020-10-01'

    ###Date Correction: If the date is not in the dataset, the closest date is found
    i = 0
    while data[data['extract_date'] == formatted_date].empty:
        formatted_date = [int(i) for i in formatted_date.split('-')]

        if month> 12:
                formatted_date[0] += 1
                month -= 11
                i= 1

        formatted_date[1] = month+i
        if formatted_date[1] <10: formatted_date = f'{formatted_date[0]}-0{formatted_date[1]}-01'
        else: formatted_date = f'{formatted_date[0]}-{formatted_date[1]}-01'
        if data[data['extract_date'] == formatted_date].empty:
            formatted_date = [int(i) for i in formatted_date.split('-')]
            formatted_date[1] = month-i
            if formatted_date[1] <10: formatted_date = f'{formatted_date[0]}-0{formatted_date[1]}-01'
            else: formatted_date = f'{formatted_date[0]}-{formatted_date[1]}-01'
        i += 1
        datecorrection = [i for i in formatted_date.split('-') if i]

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
            # Interpolate between orange and red
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
            # Interpolate between orange and red
            color = [int((1 - 2 * (normalized_elevation - 0.5)) * orange[i] + 2 * (normalized_elevation - 0.5) * red[i]) for i in range(3)]
        
        return color[1]
    
    #Filters
    #filter = 1 means on, filter = 0 means off THIS IS SPECIFIC TO LOCATION FILTERS NOT SEX, AGE OR DATE
    filter = 0
    

    fdata = data[data['sex'] == sexChoice]
    fdata = fdata[fdata['extract_date'] == formatted_date]
    if [selected_layer == 'lad' or selected_layer == 'itl'] and filter == 1:
        fdata = fdata[fdata['Region'] == 'London']
        if selected_layer == 'lad':
            fdata = fdata[fdata['ITL'] == fdata['ITL']]
    
    
    for remove_value in remove_values:
            if selected_layer == 'lad':
                fdata_filtered = fdata[fdata['LAD'].str.contains(remove_value)]
            elif selected_layer == 'itl':
                fdata_filtered = fdata[fdata['ITL'].str.contains(remove_value)]
            elif selected_layer == 'rgn':
                fdata_filtered = fdata[fdata['Region'].str.contains(remove_value)]
            
            # Check if any rows are removed
            if not fdata_filtered.empty:
                # Remove rows
                fdata = fdata[~fdata.index.isin(fdata_filtered.index)]
                message = f"{','.join([i for i in remove_values])} hidden"
            else:
                # Set message if no rows are removed
                message = f"Location {remove_value} not found in the {selected_layer}"

            

    

    fdata['elevation'] = fdata.apply(calculate_elevation_in_range, axis=1)

    max_elevation = fdata['elevation'].max()
    min_elevation = fdata['elevation'].min()

    scale = 80000 / max_elevation
    fdata['red'] = fdata['elevation'].apply(interpolate_colour_r)
    fdata['green'] = fdata['elevation'].apply(interpolate_colour_g)
    
    trends = trends_box(sexChoice,formatted_date,selected_layer)
    print(fdata)

    age_columns = fdata.filter(like='age').columns

    # Summing up values across age columns for each row
    fdata['total_population'] = fdata[age_columns].sum(axis=1)

    # Summing up the total population across all rows
    pop = round(fdata['total_population'].sum())

    # Pass processed data to template
    return render_template('map.html', DATA=fdata.to_dict(orient='records'), start_age=start_age, end_age=end_age, max_elevation=max_elevation, min_elevation=min_elevation, scale=scale, selected_layer=selected_layer, message=message, radius=radius,datecorrection = datecorrection, trends = trends, pop = pop)



if __name__ == '__main__':
    app.run(debug=True)
