from flask import Flask, render_template, request, make_response, g
from redis import Redis
import os
import socket
import random
import json
import logging

option_a = os.getenv("OPTION_A", "default_a")
option_b = os.getenv("OPTION_B", "default_b")

hostname = socket.gethostname()

app = Flask(__name__)

# Set up logging with Gunicorn
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_logger.handlers)
app.logger.setLevel(logging.DEBUG)

def get_redis_connection():
    if 'redis_conn' not in g:
        try:
            # Try localhost first, or 'redis' if running in Docker
            g.redis_conn = Redis(host='localhost', port=6379, db=0)
            # Test connection
            g.redis_conn.ping()
        except:
            app.logger.warning("Redis not available, using mock")
            g.redis_conn = None
    return g.redis_conn

@app.route('/', methods=['GET', 'POST'])
def hello():
    voter_id = request.cookies.get('voter_id')
    if not voter_id:
        voter_id = hex(random.randint(0x10000, 0x1000000))

    vote = None
    if request.method == 'POST':
        vote = request.form.get('vote')
        redis_conn = get_redis_connection()
        app.logger.info(f"Voter ID: {voter_id} voted for: {vote}")
        
        if redis_conn:
            data = json.dumps({'voter_id': voter_id, 'vote': vote})
            redis_conn.rpush('votes', data)
        else:
            app.logger.warning("Redis not available, vote not stored")

    response = make_response(render_template('index.html', option_a=option_a, option_b=option_b, hostname=hostname, vote=vote))
    response.headers['X-Option-A'] = option_a
    response.headers['X-Option-B'] = option_b
    response.set_cookie('voter_id', voter_id)
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)