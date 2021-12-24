from flask import Flask, render_template

app = Flask(__name__, template_folder="templates")


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html', size=range(15))


if __name__ == '__main__':
    app.run()
