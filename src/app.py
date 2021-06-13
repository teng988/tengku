import os
import json
from flask import Flask, render_template, request

# Local Imports
from cron import CronJob

app = Flask(__name__)


def checkPresense(fileName):
    for i in os.listdir():
        if i == fileName:
            return True
            break
        else:
            return False


def saveParams(params):
    if not os.path.isdir('config'):
        os.mkdir('config')
    with open('config/configuration.json', 'w') as f:
        json.dump(params, f)
    return True


def setCron(time, cmd):
    hr, min = time.split(':')[0], time.split(':')[1]
    print("The Hr - {hr} and the Minute is - {min}")
    obj = CronJob(hr, min)
    if cmd == 'make':
        obj.make()
    if cmd == 'update':
        obj.update()
    if cmd == 'remove':
        obj.remove()
    if cmd == 'showjobs':
        obj.show()


@app.route('/')
def getData():
    return render_template('index.html')


@app.route('/submit', methods=['GET', 'POST'])
def showData():
    if request.method == 'POST':
        params = {
            'chans': int(request.form['chans']),
            'samp_rate': int(request.form['samp_rate']),
            'chunk': int(request.form['chunk']),
            'record_secs': int(request.form['record_secs']),
            'time': request.form['time'],
            'cmd': request.form['cmds'],
            'dev_index': int(request.form['dev_index'])
        }
        print(params)
        setCron(params["time"], params['cmd'])
        if saveParams(params):
            return render_template('submit.html', result='Configuration Saved')


if __name__ == '__main__':
    app.run(debug=True)
