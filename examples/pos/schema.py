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
    created_by: Mapped[str] = mapped_column(sa.String, unique=False, nullable=True)
    deleted: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    drug_index_id: Mapped[str] = mapped_column(sa.String, unique=False, nullable=True)
    image_url: Mapped[str] = mapped_column(sa.String, unique=False, nullable=True)
    name_ar: Mapped[str] = mapped_column(sa.String, unique=False, nullable=True)
    name_en: Mapped[str] = mapped_column(sa.String, unique=False, nullable=True)
    points: Mapped[int] = mapped_column(sa.Integer, default=0)
    price: Mapped[float] = mapped_column(sa.Float, unique=False, nullable=True)
    taxable: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime, default=datetime.now()
    )
    updated_by: Mapped[str] = mapped_column(sa.String, unique=False, nullable=True)
    workspace_id: Mapped[int] = mapped_column(sa.Integer)
    international_barcode: Mapped[str] = mapped_column(sa.String, unique=False, nullable=True)
    manufacture: Mapped[str] = mapped_column(sa.String, unique=False, nullable=True)
    owner: Mapped[str] = mapped_column(sa.String, unique=False, nullable=True)
    form: Mapped[str] = mapped_column(sa.String, unique=False, nullable=True)
    number_of_strips: Mapped[int] = mapped_column(sa.Integer)
    in_store_points: Mapped[int] = mapped_column(sa.Integer)
    online_store_points: Mapped[int] = mapped_column(sa.Integer)
    insurance_points: Mapped[int] = mapped_column(sa.Integer)
    can_divide: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    gtn: Mapped[str] = mapped_column(sa.String, unique=False, nullable=True)
    tax_value_percent: Mapped[int] = mapped_column(sa.Integer, default=0)
    old_barcode: Mapped[str] = mapped_column(sa.String, unique=False, nullable=True)


class ActiveIngredient(Base):
    __tablename__ = "active_ingredient"
    __table_args__ = (UniqueConstraint("id"),)
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    concentration: Mapped[str] = mapped_column(sa.String, unique=False, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime, default=datetime.now()
    )
    created_by: Mapped[str] = mapped_column(sa.String, unique=False, nullable=True)
    deleted: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    drug_index_id: Mapped[str] = mapped_column(sa.String, unique=False, nullable=True)
    name: Mapped[str] = mapped_column(sa.String, unique=False, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime, default=datetime.now()
    )
    updated_by: Mapped[str] = mapped_column(sa.String, unique=False, nullable=True)
    workspace_id: Mapped[int] = mapped_column(sa.Integer)

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
    

class Tag(Base):
    __tablename__ = "tag"
    __table_args__ = (UniqueConstraint("id"),)
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    deleted: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    name: Mapped[str] = mapped_column(sa.String, unique=False, nullable=True)
    workspace_id: Mapped[int] = mapped_column(sa.Integer)

class ItemTags(Base):
    __tablename__ = "item_tags"
    __table_args__ = (UniqueConstraint("id"),)
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    workspace_id: Mapped[int] = mapped_column(sa.Integer)
    item_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey(Item.id))
    item: Mapped[Item] = sa.orm.relationship(
        Item,
        backref=sa.orm.backref("items"),
    )
    tag_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey(Tag.id))
    tags: Mapped[Tag] = sa.orm.relationship(
        Tag,
        backref=sa.orm.backref("tags"),
    )

class Utilization(Base):
    __tablename__ = "utilization"
    __table_args__ = (UniqueConstraint("id"),)
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime, default=datetime.now()
    )
    created_by: Mapped[str] = mapped_column(sa.String, unique=False, nullable=True)
    deleted: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    drug_index_id: Mapped[str] = mapped_column(sa.String, unique=False, nullable=True)
    name: Mapped[str] = mapped_column(sa.String, unique=False, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime, default=datetime.now()
    )
    updated_by: Mapped[str] = mapped_column(sa.String, unique=False, nullable=True)
    workspace_id: Mapped[int] = mapped_column(sa.Integer)

class ItemUses(Base):
    __tablename__ = "item_uses"
    __table_args__ = (UniqueConstraint("id"),)
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    workspace_id: Mapped[int] = mapped_column(sa.Integer)
    item_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey(Item.id))
    item: Mapped[Item] = sa.orm.relationship(
        Item,
        backref=sa.orm.backref("items"),
    )
    use_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey(Utilization.id))
    utilizations: Mapped[Utilization] = sa.orm.relationship(
        Utilization,
        backref=sa.orm.backref("utilizations"),
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
    teardown(drop_db=False,truncate_db=False,delete_redis=True,drop_index=True,delete_checkpoint=True,config=config,validate=False)
    setup(config)


if __name__ == "__main__":
    main()
