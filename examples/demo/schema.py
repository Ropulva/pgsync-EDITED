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
    name: Mapped[str] = mapped_column(sa.String, unique=False, nullable=True)
    price: Mapped[float] = mapped_column(sa.Float, unique=False, nullable=True)
    expired_at: Mapped[datetime] = mapped_column(
        sa.DateTime, default=datetime.now()
    )
    deleted: Mapped[bool] = mapped_column(sa.Boolean, default=False)


class Uses(Base):
    __tablename__ = "uses"
    __table_args__ = (UniqueConstraint("id"),)
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    usage: Mapped[str] = mapped_column(sa.String, unique=False, nullable=True)
    side_effects: Mapped[str] = mapped_column(sa.String, unique=False, nullable=True)
    item_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey(Item.id))
    item: Mapped[Item] = sa.orm.relationship(
        Item,
        backref=sa.orm.backref("items"),
    )
    


def setup(config: str) -> None:
    for doc in config_loader(config):
        database: str = doc.get("database", doc["index"])
        create_database(database)
        with pg_engine(database) as engine:
            Base.metadata.drop_all(engine)
            Base.metadata.create_all(engine)


@click.command()
@click.option(
    "--config",
    "-c",
    help="Schema config",
    type=click.Path(exists=True),
)
def main(config: str) -> None:
    config: str = get_config(config)
    teardown(drop_db=False,truncate_db=False,delete_redis=True,drop_index=True,delete_checkpoint=False,config=config,validate=False)
    setup(config)


if __name__ == "__main__":
    main()
