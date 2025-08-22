import random
from decimal import Decimal
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from models import *

def insert_test_data(engine):
    """Функция для заполнения базы данных тестовыми данными"""
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Создаем тестовых пользователей
        test_users = [
            User(
                telegram_id=123456789,
                username="test_user_1",
                first_name="Иван",
                last_name="Тестовый",
                balance=Decimal('50.0')
            ),
            User(
                telegram_id=987654321,
                username="test_user_2",
                first_name="Мария",
                last_name="Примерова",
                balance=Decimal('100.0')
            ),
            User(
                telegram_id=555555555,
                username="test_user_3",
                first_name="Алексей",
                last_name="Демо",
                balance=Decimal('25.5')
            )
        ]
        
        session.add_all(test_users)
        session.flush()  # Получаем ID пользователей
        
        # Создаем контейнеры
        containers = [
            Container(
                name="Бронзовый сундук",
                description="Небольшой сундук с умеренными наградами",
                price=Decimal('5.0'),
                is_active=True
            ),
            Container(
                name="Серебряный сундук",
                description="Сундук среднего уровня с хорошими наградами",
                price=Decimal('15.0'),
                is_active=True
            ),
            Container(
                name="Золотой сундук",
                description="Редкий сундук с щедрыми наградами",
                price=Decimal('30.0'),
                is_active=True
            ),
            Container(
                name="Неактивный сундук",
                description="Этот сундук временно недоступен",
                price=Decimal('100.0'),
                is_active=False
            )
        ]
        
        session.add_all(containers)
        session.flush()  # Получаем ID контейнеров
        
        # Создаем ячейки для контейнеров с разными вероятностями и наградами
        container_cells = [
            # Бронзовый сундук (5 TON)
            ContainerCell(container_id=containers[0].id, reward_amount=Decimal('2.0'), probability=Decimal('0.5')),
            ContainerCell(container_id=containers[0].id, reward_amount=Decimal('5.0'), probability=Decimal('0.3')),
            ContainerCell(container_id=containers[0].id, reward_amount=Decimal('10.0'), probability=Decimal('0.15')),
            ContainerCell(container_id=containers[0].id, reward_amount=Decimal('20.0'), probability=Decimal('0.05')),
            
            # Серебряный сундук (15 TON)
            ContainerCell(container_id=containers[1].id, reward_amount=Decimal('5.0'), probability=Decimal('0.4')),
            ContainerCell(container_id=containers[1].id, reward_amount=Decimal('15.0'), probability=Decimal('0.3')),
            ContainerCell(container_id=containers[1].id, reward_amount=Decimal('30.0'), probability=Decimal('0.2')),
            ContainerCell(container_id=containers[1].id, reward_amount=Decimal('50.0'), probability=Decimal('0.1')),
            
            # Золотой сундук (30 TON)
            ContainerCell(container_id=containers[2].id, reward_amount=Decimal('10.0'), probability=Decimal('0.3')),
            ContainerCell(container_id=containers[2].id, reward_amount=Decimal('35.0'), probability=Decimal('0.3')),
            ContainerCell(container_id=containers[2].id, reward_amount=Decimal('75.0'), probability=Decimal('0.25')),
            ContainerCell(container_id=containers[2].id, reward_amount=Decimal('150.0'), probability=Decimal('0.15'))
        ]
        
        session.add_all(container_cells)
        session.flush()
        
        # Создаем несколько историй открытий контейнеров
        openings = []
        for i in range(20):
            user = random.choice(test_users)
            container = random.choice(containers[:3])  # Только активные контейнеры
            cell = random.choice([c for c in container_cells if c.container_id == container.id])
            
            # Создаем открытие с датой в прошлом (для тестирования истории)
            opening_time = datetime.utcnow() - timedelta(days=random.randint(1, 30))
            
            openings.append(ContainerOpening(
                user_id=user.id,
                container_id=container.id,
                cell_id=cell.id,
                opened_at=opening_time
            ))
        
        session.add_all(openings)
        
        # Создаем тестовые транзакции
        transactions = []
        for user in test_users:
            # Делаем несколько депозитов для каждого пользователя
            for i in range(3):
                transactions.append(Transaction(
                    user_id=user.id,
                    type=TransactionType.DEPOSIT,
                    amount=Decimal(random.randint(10, 100)),
                    description=f"Депозит #{i+1}",
                    created_at=datetime.utcnow() - timedelta(days=random.randint(10, 30)),
                    status="completed"
                ))
            
            # Добавляем транзакции за открытие контейнеров
            user_openings = [o for o in openings if o.user_id == user.id]
            for opening in user_openings:
                container = session.query(Container).get(opening.container_id)
                cell = session.query(ContainerCell).get(opening.cell_id)
                
                # Транзакция списания за открытие контейнера
                transactions.append(Transaction(
                    user_id=user.id,
                    type=TransactionType.CONTAINER_PURCHASE,
                    amount=-container.price,
                    description=f"Открытие контейнера {container.name}",
                    created_at=opening.opened_at,
                    status="completed"
                ))
                
                # Транзакция награды из контейнера
                transactions.append(Transaction(
                    user_id=user.id,
                    type=TransactionType.REWARD,
                    amount=cell.reward_amount,
                    description=f"Награда из {container.name}",
                    created_at=opening.opened_at,
                    status="completed"
                ))
        
        session.add_all(transactions)
        
        # Фиксируем все изменения
        session.commit()
        print("Тестовые данные успешно добавлены в базу данных!")
        
    except Exception as e:
        session.rollback()
        print(f"Ошибка при добавлении тестовых данных: {e}")
        raise
    finally:
        session.close()