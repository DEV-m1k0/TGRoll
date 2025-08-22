from flask import Flask, render_template, request, Response, jsonify
from models import *
import random
from database import engine, create_db
from sqlalchemy.orm import Session
import requests

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

@app.route("/api/container/<int:container_id>")
def get_container_details(container_id: int):
    try:
        with Session(engine) as session:
            container = session.query(Container).filter(Container.id == container_id).first()
            if not container:
                return jsonify({"error": "Container not found"}), 404
            
            # Получаем все ячейки для этого контейнера
            cells = session.query(ContainerCell).filter(ContainerCell.container_id == container_id).all()
            
            cells_data = []
            for cell in cells:
                cells_data.append({
                    "reward_amount": float(cell.reward_amount),
                    "probability": float(cell.probability)
                })
            
            return jsonify({
                "id": container.id,
                "name": container.name,
                "description": container.description,
                "price": float(container.price),
                "cells": cells_data
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/ton_price")
def get_ton_price():
    try:
        # Используем API для получения текущего курса TON
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=the-open-network&vs_currencies=usd')
        data = response.json()
        ton_price_usd = data['the-open-network']['usd']
        return jsonify({"ton_price_usd": ton_price_usd})
    except:
        # Fallback значение в случае ошибки
        return jsonify({"ton_price_usd": 2.5})
    
@app.route("/api/open_container", methods=["POST"])
def open_container():
    try:
        data = request.get_json()
        container_id = data.get("container_id")
        
        with Session(engine) as session:
            # В реальном приложении здесь должна быть аутентификация
            # Для демонстрации используем первого пользователя
            user = session.query(User).first()
            if not user:
                return jsonify({"error": "User not found"}), 404
            
            container = session.query(Container).filter(Container.id == container_id).first()
            if not container:
                return jsonify({"error": "Container not found"}), 404
            
            if not container.is_active:
                return jsonify({"error": "Container is not active"}), 400
            
            # Проверяем баланс (преобразуем к Decimal для точных вычислений)
            from decimal import Decimal
            container_price = Decimal(str(container.price))
            
            if user.balance < container_price:
                return jsonify({"error": "Insufficient balance"}), 400
            
            # Выбираем случайную ячейку на основе вероятностей
            cells = session.query(ContainerCell).filter(ContainerCell.container_id == container_id).all()
            if not cells:
                return jsonify({"error": "No cells found for this container"}), 400
            
            # Создаем взвешенный список на основе вероятностей
            weighted_cells = []
            for cell in cells:
                weight = int(cell.probability * 100)  # Преобразуем вероятность в целое число (процент)
                weighted_cells.extend([cell] * weight)
            
            # Выбираем случайную ячейку
            selected_cell = random.choice(weighted_cells)
            
            # Создаем запись об открытии
            opening = ContainerOpening(
                user_id=user.id,
                container_id=container.id,
                cell_id=selected_cell.id
            )
            session.add(opening)
            
            # Создаем транзакцию для списания средств
            purchase_transaction = Transaction(
                user_id=user.id,
                type=TransactionType.CONTAINER_PURCHASE,
                amount=-container_price,
                description=f"Purchase of {container.name}"
            )
            session.add(purchase_transaction)
            
            # Создаем транзакцию для награды
            reward_amount = Decimal(str(selected_cell.reward_amount))
            reward_transaction = Transaction(
                user_id=user.id,
                type=TransactionType.REWARD,
                amount=reward_amount,
                description=f"Reward from {container.name}"
            )
            session.add(reward_transaction)
            
            # Обновляем баланс пользователя
            user.balance = user.balance - container_price + reward_amount
            
            session.commit()
            
            return jsonify({
                "reward": float(reward_amount),
                "probability": float(selected_cell.probability),
                "new_balance": float(user.balance)
            })
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    
@app.route("/api/user_balance")
def get_user_balance():
    try:
        with Session(engine) as session:
            # Для демонстрации используем первого пользователя
            user = session.query(User).first()
            if not user:
                return jsonify({"error": "User not found"}), 404
            
            return jsonify({
                "balance": float(user.balance)
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def run_app():
    app.run(debug=True, host="0.0.0.0", port=1234)


if __name__ == "__main__":
    # create_db()
    run_app()