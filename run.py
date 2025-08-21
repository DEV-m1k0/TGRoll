from main import run_app
from data import create_test_containers
from database import create_db


if __name__ == "__main__":
    create_db()
    create_test_containers()
    run_app()