from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/map_explorer')
def map_explorer():
    return render_template('map_explorer.html')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/snapshot')
def snapshot():
    return render_template('snapshot.html')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

if __name__ == '__main__':
    app.run(debug=True)
