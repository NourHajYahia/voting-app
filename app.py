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
    dog_votes = int(r.get('dog') or 0)
    cat_votes = int(r.get('cat') or 0)
    print("dogs votes are: %d , cats votes are: %d" % (dog_votes, cat_votes))
    return render_template('index.html')
    

@app.route('/reset')
def reset():
    r.set('dog', 0)
    r.set('cat', 0)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)

