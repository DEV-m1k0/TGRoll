from flask import Flask, render_template, request, Response, redirect, url_for
from models import Container
from database import engine, create_db
from sqlalchemy.orm import Session
from api import get_estimated_price
import requests, os



app = Flask(__name__, template_folder="./templates")

@app.route("/")
def index():
    try:
        with Session(engine) as session:
            containers = session.query(Container).all()
    except:
        containers = []

    return render_template("index.html", containers=containers)

@app.route("/", methods=['POST'])
def index_post():
    amount_of_ton = float(request.form.get("amount"))
    redirect_to_pay = create_invoice(amount_of_ton, request.url)
    if redirect_to_pay:
        return redirect(redirect_to_pay)
    return redirect(url_for("index"))


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


# API
def create_invoice(ton_amount: int|float, domain_url, order_description: None|str = None):
    price_amount = get_estimated_price(ton_amount)
    if price_amount:
        x_api_key = os.getenv("api_private_key")
        response = requests.post(
            url=f"https://api.nowpayments.io/v1/invoice",
            headers={
                "x-api-key": x_api_key
            },
            json={
                    "price_amount": price_amount, 
                    "price_currency": "usd",
                    "pay_currency": "ton",
                    "order_description": f"{order_description}",
                    "ipn_callback_url": domain_url,
                    "success_url": domain_url,
                    "cancel_url": domain_url
            }
        )
        if response.status_code == 200:
            return response.json()['invoice_url']
    return False


def run_app():
    app.run(debug=True, host="0.0.0.0", port=1234)


if __name__ == "__main__":
    run_app()