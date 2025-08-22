from flask import Flask, render_template, request
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


@app.route("/containers")
def container_detail():
    container_id = request.args.get('container_id')
    print(container_id)
    return render_template("index.html")


def run_app():
    app.run(debug=False, host="0.0.0.0", port=1234)


if __name__ == "__main__":
    run_app()