from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/account')
def account():
    return render_template('account-page.html')

@app.route('/analytics')
def analytics():
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
