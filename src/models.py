import enum
import logging
import random
from _decimal import Decimal

from faker import Faker
from json import JSONEncoder

from pydantic.json import pydantic_encoder

from sqlalchemy import Column, String, ARRAY
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import Enum, Integer, Numeric

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


class CurrencyTypes(enum.Enum):
    RUB = 'rub'
    USD = 'usd'
    EUR = 'eur'


class FuelTypes(enum.Enum):
    GASOLINE76 = '76'
    GASOLINE80 = '80'
    GASOLINE91 = '91'
    GASOLINE92 = '92'
    GASOLINE95 = '95'
    GASOLINE100 = '100'
    GASOLINE105 = '105'
    DIESEL = 'diesel'
    DIESEL_WINTER = 'diesel_winter'
    AD_BLUE = 'ad_blue'


class AZSMainInfo(Base):
    __tablename__ = 'azs_main_info'

    id = Column(Integer, nullable=False, primary_key=True, comment='id Заправочной станции')
    tel_number = Column(String(20), comment='Номер телефона')
    coords = Column(String(255), comment='Координаты АЗС')
    address = Column(String(255), comment='Адрес АЗС')
    images = Column(ARRAY(item_type=String), comment='Изображения')
    services = Column(ARRAY(item_type=String), comment='Дополнительные Услуги')
    # Faker будет сохранять сюда случайные слова


class AZSFuelInfo(Base):
    __tablename__ = 'azs_fuel_info'

    id = Column(Integer, nullable=False, primary_key=True, comment='id Заправочной станции')
    price = Column(Numeric(scale=2), comment='Цена топлива')
    type = Column(Enum(FuelTypes), comment='Тип топлива')
    currency = Column(Enum(CurrencyTypes), comment='Тип валюты')


async def create_azs_main_info(db: Session, azs_obj: AZSMainInfo | AZSFuelInfo):
    db.add(azs_obj)
    db.commit()


fake = Faker()

async def create_test_data():
    logger.info('Старт создания тестовых данных')
    for azs_id in range(10001):
        tel_number = fake.phone_number()
        coords = f'{fake.latitude()}, {fake.longitude()}'
        address = fake.address()
        images = [fake.image_url() for _ in range(random.randint(1, 5))]
        services = [fake.word() for _ in range(random.randint(1, 10))]

        azs_main_info = AZSMainInfo(
            id=azs_id, tel_number=tel_number, coords=coords, address=address, images=images, services=services
        )

        with SessionLocal() as session:
            await create_azs_main_info(session, azs_main_info)
            logger.info(f'АЗС с id{azs_id} сохранен в AZSMainInfo')

        fuel_type = random.choice(list(FuelTypes))
        # price = round(random.uniform(1.0, 150), 2)
        currency = random.choice(list(CurrencyTypes))
        if currency == CurrencyTypes.RUB:
            price = round(random.uniform(40.0, 130), 2)
        else:
            price = round(random.uniform(0.25, 4.0), 2)

        azs_fuel_info = AZSFuelInfo(id=azs_id, type=fuel_type, price=price, currency=currency)

        with SessionLocal() as session:
            await create_azs_main_info(session, azs_fuel_info)
            logger.info(f'АЗС с id{azs_id} сохранен в AZSMainInfo')
    logger.info('Завершение создания тестовых данных')
