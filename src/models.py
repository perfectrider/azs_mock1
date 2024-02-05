# import logging
import logging
import random

from faker import Faker
from json import JSONEncoder

from pydantic.json import pydantic_encoder

from sqlalchemy import Column, String, ARRAY, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import Integer, Numeric

from src.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger()


DSN = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


class CustomEncoder(JSONEncoder):
    def __init__(self, *args, **kwargs):
        kwargs['default'] = pydantic_encoder
        super().__init__(*args, **kwargs)


engine = create_engine(DSN, echo=True, pool_pre_ping=True, json_serializer=CustomEncoder().encode)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
session = Session


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class AZSMainInfo(Base):
    __tablename__ = 'azs_main_info'

    id = Column(Integer, nullable=False, primary_key=True, comment='id Заправочной станции')
    tel_number = Column(String(255), comment='Номер телефона')
    coords = Column(String(255), comment='Координаты АЗС')
    address = Column(String(255), comment='Адрес АЗС')
    images = Column(ARRAY(item_type=String), comment='Изображения')
    services = Column(ARRAY(item_type=String), comment='Дополнительные Услуги')


class AZSFuelInfo(Base):
    __tablename__ = 'azs_fuel_info'

    id = Column(Integer, nullable=False, primary_key=True, comment='id Заправочной станции')


class Fuel(Base):
    __tablename__ = 'fuel'

    id = Column(Integer, primary_key=True)
    price = Column(Numeric(scale=2), comment='Цена топлива')
    type = Column(String(255), comment='Тип топлива')
    currency = Column(String(255), comment='Тип валюты')
    location = Column(ForeignKey('azs_fuel_info.id', ondelete='CASCADE'), comment='Топливо текущей заправки')


async def create_azs_info(db: Session, azs_obj: AZSMainInfo | AZSFuelInfo):
    db.add(azs_obj)
    db.commit()


async def create_fuel_info(db: Session, fuel_obj: Fuel):
    db.add(fuel_obj)
    db.commit()


fake = Faker()

fuel_prices = {
    'gas92': ['rub', 50.0],
    'gas95': ['rub', 55.0],
    'diesel': ['rub', 60.0],
}

async def create_test_data():
    logger.info('Старт создания тестовых данных')
    for azs_id in range(10):
        tel_number = fake.phone_number()
        coords = f'{fake.latitude()}, {fake.longitude()}'
        address = fake.address()
        images = [fake.image_url() for _ in range(random.randint(1, 5))]
        services = [fake.word() for _ in range(random.randint(1, 10))]

        azs_main_info = AZSMainInfo(
            id=azs_id, tel_number=tel_number, coords=coords, address=address, images=images, services=services
        )

        with SessionLocal() as session:
            await create_azs_info(session, azs_main_info)
            logger.info(f'АЗС с id{azs_id} сохранен в AZSMainInfo')

        azs_fuel_info = AZSFuelInfo(id=azs_id)

        with SessionLocal() as session:
            await create_azs_info(session, azs_fuel_info)
            logger.info(f'АЗС с id{azs_id} сохранен в AZSMainInfo')

        for key, value in fuel_prices.items():
            fuel_type = key
            currency = value[0]
            price = value[1]

            fuel_info = Fuel(price=price, type=fuel_type, currency=currency, location=azs_id)

            with SessionLocal() as session:
                await create_fuel_info(session, fuel_info)
                logger.info(f'Fuel сохранен в Fuel для АЗС id-{azs_id}')

    logger.info('Завершение создания тестовых данных')
