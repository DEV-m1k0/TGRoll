from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Float



class Base(DeclarativeBase):
    pass


class Container(Base):
    __tablename__ = "container"

    id: Mapped[int] = mapped_column(primary_key=True)
    image: Mapped[str] = mapped_column(String(1))
    title: Mapped[str] = mapped_column(String(20))
    price: Mapped[float] = mapped_column(Float())

    def __repr__(self):
        return f"Contaier(id={self.id!r}, title={self.title!r}, price={self.price!r})"