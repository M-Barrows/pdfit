from datetime import datetime
from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column, Mapped
from sqlalchemy import Table, Column, ForeignKey, func


class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

doc_img_association = Table(
    "doc_img_association",
    Base.metadata,
    Column("doc_id", ForeignKey("documents.id"), primary_key=True),
    Column("img_id", ForeignKey("images.id"), primary_key=True),
)

class Document(db.Model):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    storage_location: Mapped[str] = mapped_column(unique=True)
    created_date: Mapped[datetime]
    images: Mapped[List["Image"]] = relationship(secondary= doc_img_association, back_populates="documents")

class Image(db.Model):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    image_url: Mapped[str] = mapped_column(unique=True)
    storage_location: Mapped[str] = mapped_column(unique=True)
    documents: Mapped[List["Document"]] = relationship(secondary= doc_img_association, back_populates="images")

