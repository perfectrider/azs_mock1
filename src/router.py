from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.models import create_test_data, get_session, AZSMainInfo, Fuel, AZSFuelInfo
from src.schemas import AZSAllMainInfoModel, AZSFuelInfoModel, FuelInfo

router = APIRouter()


@router.get('/main_info', response_model=List[AZSAllMainInfoModel])
async def get_main_info(db: Session = Depends(get_session)):
    q = db.query(AZSMainInfo)
    azs_main_objects = []
    for obj in q.all():
        _ = AZSAllMainInfoModel.from_orm(obj)
        azs_main_objects.append(_)
    return azs_main_objects

@router.get('/fuel_info', response_model=List[AZSFuelInfoModel])
async def get_fuel_info(db: Session = Depends(get_session)):

    q = db.query(AZSFuelInfo).all()
    for azs_fuel_info in q:
        fuels = db.query(Fuel).filter(Fuel.location == azs_fuel_info.id).all()
        fuel_data_list = []
        for fuel in fuels:
            _ = FuelInfo.from_orm(fuel)
            fuel_data_list.append(_)

        azs_fuel_info.fuels = fuel_data_list

    azs_fuel_objects = []
    for obj in q:
        _ = AZSFuelInfoModel.from_orm(obj)
        azs_fuel_objects.append(_)

    return azs_fuel_objects


@router.post('/createdata')
async def create_data() -> str:
    await create_test_data()
    return 'Тестовые данные успешно сохранены'

