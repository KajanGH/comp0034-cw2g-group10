import pandas as pd
import matplotlib.pyplot as plt
import calendar
import secrets
from flask import Flask, render_template, request, session
from collections import deque
from helpers import encode_auth_token, token_required

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Load data
lad_url = 'https://media.githubusercontent.com/media/KajanGH/data/main/prepared_lad.csv'
lad_csv = pd.read_csv(lad_url)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/account')
@token_required
def account():
    return render_template('account-page.html')

search = deque(["","",""],maxlen=3)
@app.route('/analytics', methods=['GET', 'POST'])
@token_required
def analytics():
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
        ###SEX PIE CHART###
        sex_age_counts = df.groupby('sex')[age_columns].sum()

        # Calculate the total number of people per sex
        total_people_per_sex = sex_age_counts.sum(axis=1)

        # Plotting
        plt.figure(figsize=(8, 8))
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
        plt.figure(figsize=(8, 8))
        plt.pie(total_people_per_location, labels=total_people_per_location.index, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 30})
        plt.title('ITL Ratio',fontsize=60)
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig('static/public/graph4.png')

        ###MONTH PIE CHART###
        month_counts = df['month'].value_counts()
        # Plotting
        plt.figure(figsize=(8, 8))
        plt.pie(month_counts, labels=month_counts.index, autopct='%1.1f%%', startangle=140,textprops={'fontsize': 25})
        plt.title('Month Ratio',fontsize=60)
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig('static/public/graph5.png')

        search.append(form)
        return render_template('analytics-page.html',DataToRender = search )
    # Render analytics page template
    return render_template('analytics-page.html',DataToRender = search )

@app.route('/dashboard')
@token_required
def dashboard():
    return render_template('dashboard-page.html')

@app.route('/log-in', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        df = pd.read_csv("dataset\\users.csv")
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

@app.route('/snapshot')
@token_required
def snapshot():
    return render_template('snapshot-page.html')

@app.route('/map')
def map():
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
    

    fdata = lad_csv[lad_csv['sex'] == 'female']
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
    return render_template('map.html', data=fdata.to_dict(orient='records'), start_age=start_age, end_age=end_age, max_elevation=max_elevation, min_elevation=min_elevation, scale=scale)



if __name__ == '__main__':
    app.run(debug=True)
