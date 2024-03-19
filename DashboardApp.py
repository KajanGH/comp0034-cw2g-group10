import pandas as pd
import matplotlib.pyplot as plt
import calendar
from flask import Flask, render_template, request
from string import capwords
from collections import deque

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/account')
def account():
    return render_template('account-page.html')

search = deque(["","",""],maxlen=3)
@app.route('/analytics', methods=['GET', 'POST'])
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
def dashboard():
    return render_template('dashboard-page.html')

@app.route('/log-in')
def login():
    return render_template('log-in-page.html')

@app.route('/settings')
def settings():
    return render_template('settings-page.html')

@app.route('/sign-up')
def signup():
    return render_template('sign-up-page.html')

@app.route('/snapshot')
def snapshot():
    return render_template('snapshot-page.html')

@app.route('/fake-graph1')
def graph1():
    return render_template('fake-graph1-popup.html')

@app.route('/fake-graph2')
def graph2():
    return render_template('fake-graph2-popup.html')

@app.route('/fake-graph3')
def graph3():
    return render_template('fake-graph3-popup.html')

@app.route('/fake-graph4')
def graph4():
    return render_template('fake-graph4-popup.html')

if __name__ == '__main__':
    app.run(debug=True)
