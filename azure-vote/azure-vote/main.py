from flask import Flask, request, make_response, render_template
import os
import redis
import socket
from multiprocessing import Pool, cpu_count
import time
import uuid


app = Flask(__name__)

# Load configurations from environment or config file
app.config.from_pyfile('config_file.cfg')

if ("VOTE1VALUE" in os.environ and os.environ['VOTE1VALUE']):
    button1 = os.environ['VOTE1VALUE']
else:
    button1 = app.config['VOTE1VALUE']

if ("VOTE2VALUE" in os.environ and os.environ['VOTE2VALUE']):
    button2 = os.environ['VOTE2VALUE']
else:
    button2 = app.config['VOTE2VALUE']

if ("TITLE" in os.environ and os.environ['TITLE']):
    title = os.environ['TITLE']
else:
    title = app.config['TITLE']

# Redis configurations
redis_server = os.environ['REDIS']
redis_tls = os.environ.get('REDIS_TLS', 'OFF')

if redis_tls == 'ON':
    redis_port = 6380
    redis_tls = True
else:
    redis_port = 6379
    redis_tls = False

hostn = os.environ.get('HOSTNAME', str(uuid.uuid4()))

# Redis Connection
try:
    if "REDIS_PWD" in os.environ:
        r = redis.StrictRedis(host=redis_server,
                              port=redis_port,
                              ssl=redis_tls,
                              password=os.environ['REDIS_PWD'])
    else:
        r = redis.Redis(redis_server)
    r.ping()
except redis.ConnectionError:
    exit('Failed to connect to Redis, terminating.')

# Change title to host name to demo NLB
if app.config['SHOWHOST'] == "true":
    title = socket.gethostname()

# Init Redis
if not r.get(button1):
    r.set(button1, 0)
if not r.get(button2):
    r.set(button2, 0)


def f(x):
    set_time = os.environ.get('STRESS_SECS', 5)
    timeout = time.time() + float(set_time)  # X seconds from now
    while True:
        if time.time() > timeout:
            break
        x * x


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # Get current values
        vote1 = r.get(button1).decode('utf-8')
        vote2 = r.get(button2).decode('utf-8')
    elif request.method == 'POST':
        if request.form['vote'] == 'reset':
            # Empty table and return results
            r.set(button1, 0)
            r.set(button2, 0)
            vote1 = r.get(button1).decode('utf-8')
            vote2 = r.get(button2).decode('utf-8')
        else:
            # Insert vote result into DB
            vote = request.form['vote']
            r.incr(vote, 1)

            # Get current values
            vote1 = r.get(button1).decode('utf-8')
            vote2 = r.get(button2).decode('utf-8')

            # Generate fake load
            processes = cpu_count()
            pool = Pool(processes)
            pool.map(f, range(processes))

    resp = make_response(render_template("index.html", value1=int(vote1), value2=int(vote2), button1=button1, button2=button2, title=title))
    resp.headers.set('X-HANDLED-BY', hostn)
    return resp


if __name__ == "__main__":
    app.run()
