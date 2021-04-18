#!/usr/bin/env python3

from flask_cors import CORS
from flask import Flask, render_template
from flask import request
from gevent.pywsgi import WSGIServer
import random, copy, json

app = Flask(__name__)
CORS(app)

with open("data.json", "r") as f:
    data = json.load(f)

original_questions = data

questions = copy.deepcopy(original_questions)

def sampling(q, n=2):
    return random.sample(list(q.keys()), n)

def translate():
    return (lambda x: "True" if x else "False")

@app.route('/')
def quiz():
 questions_shuffled = sampling(questions)
 return render_template('main.html', q = questions_shuffled, o = questions)

@app.route('/quiz', methods=['POST'])
def quiz_answers():
    result = "<ol>"
    correct = 0
    for i in questions.keys():
        if i in request.form:
            answered = request.form[i]
            if original_questions[i][answered]:
                result += "<li><u>{}</u></li>{} <b>{}</b>".format(i, answered, translate()(original_questions[i][answered]))
                correct = correct+1
            else:
                result += "<li><u>{}</u></li>{} <b>{}</b>".format(i, answered, translate()(original_questions[i][answered]))
    result += "</ol>"
    result += '<h1>Risposte corrette: <u>'+str(correct)+'</u></h1>'
    return result

if __name__ == "__main__":
    app.debug = True
    http_server = WSGIServer(('', 8000), app)
    http_server.serve_forever()
