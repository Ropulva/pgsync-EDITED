from datetime import datetime

import click
import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.schema import UniqueConstraint

from pgsync.base import create_database, pg_engine
from pgsync.helper import teardown
from pgsync.utils import config_loader, get_config


class Base(DeclarativeBase):
    pass


class Item(Base):
    __tablename__ = "item"
    __table_args__ = (UniqueConstraint("id"),)
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime, default=datetime.now()
    )
    deleted: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    name_en: Mapped[str] = mapped_column(sa.String, unique=False, nullable=True)
    points: Mapped[int] = mapped_column(sa.Integer, default=0)


class ActiveIngredient(Base):
    __tablename__ = "active_ingredient"
    __table_args__ = (UniqueConstraint("id"),)
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    deleted: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    name: Mapped[str] = mapped_column(sa.String, unique=False, nullable=True)

class ItemActiveIngredients(Base):
    __tablename__ = "item_active_ingredients"
    __table_args__ = (UniqueConstraint("id"),)
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    workspace_id: Mapped[int] = mapped_column(sa.Integer)
    item_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey(Item.id))
    item: Mapped[Item] = sa.orm.relationship(
        Item,
        backref=sa.orm.backref("items"),
    )
    active_ingredient_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey(ActiveIngredient.id))
    active_ingredients: Mapped[ActiveIngredient] = sa.orm.relationship(
        ActiveIngredient,
        backref=sa.orm.backref("active_ingredients"),
    )
    

@click.command()
@click.option(
    "--config",
    "-c",
    help="Schema config",
    type=click.Path(exists=True),
)
def main(config: str) -> None:
    config: str = get_config(config)
    teardown(drop_db=False,truncate_db=False,delete_redis=True,drop_index=True,delete_checkpoint=True,config=config,validate=False)


if __name__ == "__main__":
    main()