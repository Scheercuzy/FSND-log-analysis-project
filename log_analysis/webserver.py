from flask import Flask, render_template
from log_analysis.__main__ import answer_all
from log_analysis.database import DBConnection
app = Flask(__name__)


@app.route('/')
@app.route('/answers')
def answers():
    with DBConnection() as conn:
        answers = answer_all(conn)
    return render_template('answers.html', answers=answers)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
