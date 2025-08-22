from flask import Flask, render_template, request, Response
from models import Container
from database import engine, create_db
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
    return render_template("index.html")


@app.route("/images/image/<int:container_id>")
def get_image(container_id: int):
    try:
        with Session(engine) as session:
            container = session.query(Container).filter(Container.id == container_id).first()
            img = container.image
            if img:
                return Response(img, mimetype='image/jpeg')
            else:
                return "Image not found", 404
    except:
        pass


def run_app():
    app.run(debug=True, host="0.0.0.0", port=1234)


if __name__ == "__main__":
    # create_db()
    run_app()