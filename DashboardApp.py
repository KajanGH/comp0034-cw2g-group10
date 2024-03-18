from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/account')
def account():
    return render_template('account-page.html')

@app.route('/analytics', methods=['GET', 'POST'])
def analytics():
    if request.method == 'POST':
        df = pd.read_csv('dataset/prepared_ctry.csv',  usecols=lambda col: 'age' in col or col in ['Country', 'extract_date', 'sex'])
        age_sum = 0
        for index,row in df.iterrows():
            df.at[index, 'year'] = int(row['extract_date'].split('-')[0])
            df.at[index, 'month'] = int(row['extract_date'].split('-')[1])
        if 'sex' in request.form.keys(): df = df[df['sex'] == request.form['sex']]
        if 'Country' in request.form.keys(): df = df[df['Country'] == request.form['Country']]
        if 'year' in request.form.keys(): df = df[df['extract_date'].str.contains(request.form['year'],na=False)]
        if 'month' in request.form.keys(): df = df[df['extract_date'].str.contains(request.form['month'],na=False)]
        if 'high-age' in request.form.keys(): high_age = int(request.form['high-age'])
        else: high_age = 95
        if 'low-age' in request.form.keys(): low_age = int(request.form['low-age'])
        else: low_age = 0
        for i in range(high_age-low_age+1):
            age_sum += df[f'age_{i+low_age}']
        df['age'] = age_sum
        age_cols_to_keep = [f'age_{i}' for i in range(low_age, high_age + 1)]
        df = df[['Country', 'sex', 'year', 'month'] + age_cols_to_keep]
        #df.to_excel(f'newdataset/{request.form}_prepared_ctry.xlsx', index=False)

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
        sex_counts = df['sex'].value_counts()

        # Plotting
        plt.figure(figsize=(8, 8))
        plt.pie(sex_counts, labels=sex_counts.index, autopct='%1.1f%%', startangle=140,textprops={'fontsize': 30})
        plt.title('Sex Ratio',fontsize=60)
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig('static/public/graph3.png')

        ###LOCATION PIE CHART###
        location_counts = df['Country'].value_counts()

        # Plotting
        plt.figure(figsize=(8, 8))
        plt.pie(location_counts, labels=location_counts.index, autopct='%1.1f%%', startangle=140,textprops={'fontsize': 30})
        plt.title('Location Ratio',fontsize=60)
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig('static/public/graph4.png')

        ###MONTH PIE CHART###
        month_counts = df['month'].value_counts()
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        # Plotting
        plt.figure(figsize=(8, 8))
        plt.pie(month_counts, labels=months, autopct='%1.1f%%', startangle=140,textprops={'fontsize': 25})
        plt.title('Month Ratio',fontsize=60)
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig('static/public/graph5.png')

        return redirect(url_for('analytics'))
    # Render analytics page template
    return render_template('analytics-page.html')

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
