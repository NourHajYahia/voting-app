from flask import Flask, render_template, redirect, url_for
import redis
import os

app = Flask(__name__)


redis_url = os.getenv('REDIS_URL', 'redis://redis:6379/0')

# Connect to Redis
r = redis.Redis.from_url(redis_url)

# Define the stream name
stream_name = 'votingstream'


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/vote/<option>')
def vote(option):
    if option.lower() == 'dog':
        r.xadd(stream_name, {'animal':'dog'})
    elif option.lower() == 'cat':
        r.xadd(stream_name, {'animal':'cat'})
    return render_template('index.html')

@app.route('/result')
def index():
    return render_template('result.html')

@app.route('/next')
def get_next_value():
    # XREAD blocks until it finds an entry
    stream_data = r.xread({stream_name: '$'}, block=0, count=1)
    
    # Assuming stream_data format: [(stream_name, [(entry_id, entry_data)])]
    # Process the entries
    for stream, messages in stream_data:
        for message_id, message_data in messages:
            print(f"ID: {message_id}")
            for key, value in message_data.items():
                print(f"{key.decode('utf-8')}: {value.decode('utf-8')}")
                return {'value': value.decode('utf-8')}

    return {'value': 'No data available'}

    

@app.route('/reset')
def reset():
    r.set('dog', 0)
    r.set('cat', 0)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)

