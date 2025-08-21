from flask import Flask, render_template
from models import Container
from database import engine
from sqlalchemy.orm import Session

app = Flask(__name__, template_folder="./templates")

@app.route("/")
def index():
    with Session(engine) as session:
        containers = session.query(Container).all()

    return render_template("index.html", containers=containers)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=1234)