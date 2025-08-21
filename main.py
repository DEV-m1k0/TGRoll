from flask import Flask, render_template
from models import Container
from database import engine
from sqlalchemy.orm import Session

app = Flask(__name__, template_folder="./templates")

@app.route("/")
def index():
    try:
        with Session(engine) as session:
            containers = session.query(Container).all()
    except:
        containers = []

    return render_template("index.html", containers=containers)


def run_app():
    app.run(debug=True, host="0.0.0.0", port=1234)