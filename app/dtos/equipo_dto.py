from typing import Optional
from pydantic import BaseModel, ConfigDict


class UserResponseDTO(BaseModel):
    id: str
    username: str
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)


class WeatherDTO(BaseModel):
    ciudad: str
    temperatura: Optional[float] = None
    viento: Optional[float] = None
    codigo_tiempo: Optional[int] = None
    instante: Optional[str] = None


class EquipoResponseDTO(BaseModel):
    id: int
    nombre: str
    ciudad: Optional[str] = None
    fundacion: Optional[int] = None
    liga: Optional[str] = None
    pabellon: Optional[str] = None
    aforo: Optional[int] = None
    cantera: bool = False
    filename: Optional[str] = None
    user: Optional[UserResponseDTO] = None
    weather: Optional[WeatherDTO] = None

    model_config = ConfigDict(from_attributes=True)


class NewEquipoDTO(BaseModel):
    nombre: str
    ciudad: Optional[str] = None
    fundacion: Optional[int] = None
    liga: Optional[str] = None
    pabellon: Optional[str] = None
    aforo: Optional[int] = None
    cantera: bool = False
    user_id: str

    model_config = ConfigDict(extra="forbid")


class EditEquipoDTO(BaseModel):
    nombre: Optional[str] = None
    ciudad: Optional[str] = None
    fundacion: Optional[int] = None
    liga: Optional[str] = None
    pabellon: Optional[str] = None
    aforo: Optional[int] = None
    cantera: Optional[bool] = None

    model_config = ConfigDict(extra="forbid")