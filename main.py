from flask import Flask, render_template

app = Flask(__name__)


@app.route("/api/v1/hello-world-<int:id>")
def hello(id):
    hello = "Hello World " + str(id)
    return render_template("index.html", hello=hello)


if __name__ == '__main__':
    app.run(debug=True)