from database import engine
from sqlalchemy.orm import Session
from models import Container


def create_test_containers():
    try:
        # Создаем сессию
        session = Session(engine)
        
        # Проверяем существующие контейнеры
        containers = session.query(Container).all()
        
        if not containers:
            # Создаем объекты контейнеров
            ordinary_container = Container(
                image="📦",
                title="Обычный контейнер",
                price=100.0
            )
            rare_container = Container(            
                image="🎁",
                title="Редкий контейнер",
                price=250.0
            )
            epic_container = Container(
                image="🧰",
                title="Эпический контейнер",
                price=500.0
            )
            legendary_container = Container(
                image="💎",
                title="Легендарный контейнер",
                price=1000.0
            )
            mythical_container = Container(
                image="🔮",
                title="Мистический контейнер",
                price=750.0
            )
            golden_container = Container(
                image="📭",
                title="Золотой контейнер",
                price=1500.0
            )
            
            # Добавляем и коммитим
            session.add_all([
                ordinary_container, 
                rare_container, 
                epic_container, 
                legendary_container, 
                mythical_container, 
                golden_container
            ])
            session.commit()
            print("Тестовые контейнеры успешно созданы!")
        else:
            print("Контейнеры уже существуют в базе данных")
            
    except Exception as e:
        # В случае ошибки откатываем изменения
        session.rollback()
        print(f"Ошибка при создании тестовых контейнеров: {e}")
        # Выводим полную трассировку для отладки
        import traceback
        traceback.print_exc()
    finally:
        # Всегда закрываем сессию
        session.close()

def remove_all_data():
    with Session(engine) as session:
        all_rows = session.query(Container).all()

        for row in all_rows:
            session.delete(row)
        
        session.commit()