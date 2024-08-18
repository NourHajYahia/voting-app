from flask import Flask, render_template, redirect, url_for
import redis

app = Flask(__name__)

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/vote/<option>')
def vote(option):
    if option.lower() == 'dog':
        r.incr('dog')
    elif option.lower() == 'cat':
        r.incr('cat')
    return redirect(url_for('results'))

@app.route('/results')
def results():
    dog_votes = int(r.get('dog') or 0)
    cat_votes = int(r.get('cat') or 0)
    return render_template('results.html', dog_votes=dog_votes, cat_votes=cat_votes)

if __name__ == "__main__":
    app.run(debug=True)

