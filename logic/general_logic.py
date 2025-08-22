from sqlalchemy import create_engine, Column, Integer, BigInteger, String, Numeric, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import enum

Base = declarative_base()

# Валюта системы
class Currency(enum.Enum):
    TON = "TON"

# Типы транзакций
class TransactionType(enum.Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    CONTAINER_PURCHASE = "container_purchase"
    REWARD = "reward"

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    balance = Column(Numeric(20, 9), default=0)  # Баланс в TON (1 TON = 10^9 наноTON)
    created_at = Column(DateTime, default=datetime.now())
    
    # Связи
    transactions = relationship("Transaction", back_populates="user")
    container_openings = relationship("ContainerOpening", back_populates="user")

class Container(Base):
    __tablename__ = 'containers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    price = Column(Numeric(20, 9), nullable=False)  # Стоимость открытия в TON
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now())
    
    # Связи
    cells = relationship("ContainerCell", back_populates="container")
    openings = relationship("ContainerOpening", back_populates="container")

class ContainerCell(Base):
    __tablename__ = 'container_cells'
    
    id = Column(Integer, primary_key=True)
    container_id = Column(Integer, ForeignKey('containers.id'), nullable=False)
    reward_amount = Column(Numeric(20, 9), nullable=False)  # Награда в TON
    probability = Column(Numeric(5, 4), default=1.0)  # Вероятность выпадения (от 0 до 1)
    
    # Связи
    container = relationship("Container", back_populates="cells")
    openings = relationship("ContainerOpening", back_populates="cell")

class ContainerOpening(Base):
    __tablename__ = 'container_openings'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    container_id = Column(Integer, ForeignKey('containers.id'), nullable=False)
    cell_id = Column(Integer, ForeignKey('container_cells.id'), nullable=False)
    opened_at = Column(DateTime, default=datetime.now())
    
    # Связи
    user = relationship("User", back_populates="container_openings")
    container = relationship("Container", back_populates="openings")
    cell = relationship("ContainerCell", back_populates="openings")

class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    amount = Column(Numeric(20, 9), nullable=False)
    currency = Column(Enum(Currency), default=Currency.TON)
    description = Column(String(500))
    created_at = Column(DateTime, default=datetime.now())
    
    # Для внешних транзакций (депозиты/выводы)
    external_address = Column(String(100))
    tx_hash = Column(String(100), unique=True)
    status = Column(String(50), default="pending")  # pending, completed, failed
    
    # Связи
    user = relationship("User", back_populates="transactions")

# Инициализация базы данных
engine = create_engine('sqlite:///crypto_bot.db')  # Для продакшена используйте PostgreSQL
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)