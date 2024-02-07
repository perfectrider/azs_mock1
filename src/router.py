from typing import List, Optional, Union

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.models import create_test_data, get_session, AZSMainInfo, Fuel, AZSFuelInfo
from src.schemas import AZSAllMainInfoModel, AZSFuelInfoModel, FuelInfo

router = APIRouter()


@router.get('/main_info', response_model=Union[List[AZSAllMainInfoModel] | AZSAllMainInfoModel])
async def get_main_info(db: Session = Depends(get_session),
                        azs_id: Optional[int] = None):
    if azs_id:
        q = db.query(AZSMainInfo).filter(AZSMainInfo.id == azs_id).first()
        return AZSAllMainInfoModel.from_orm(q)

    q = db.query(AZSMainInfo).all()
    azs_main_objects = []
    for obj in q:
        _ = AZSAllMainInfoModel.from_orm(obj)
        azs_main_objects.append(_)
    return azs_main_objects


@router.get('/fuel_info', response_model=Union[List[AZSFuelInfoModel] | AZSFuelInfoModel])
async def get_fuel_info(db: Session = Depends(get_session),
                        azs_id: Optional[int] = None):

    if azs_id:
        q = db.query(AZSFuelInfo).filter(AZSFuelInfo.id == azs_id)
    else:
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

    adjusted = azs_fuel_objects[0] if azs_id else azs_fuel_objects
    return adjusted


@router.post('/create_main_info')
async def create_main_info(**kwargs):
    pass


@router.post('/create_fuel_info')
async def create_main_info(**kwargs):
    pass


@router.post('/createdata')
async def create_data() -> str:
    await create_test_data()
    return 'Тестовые данные успешно сохранены'

