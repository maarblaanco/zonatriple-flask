from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from database import db
from models.equipo import Equipo
from dtos.equipo_dto import EquipoResponseDTO, NewEquipoDTO, EditEquipoDTO
from logger import logger
from services.weather_service import get_weather_by_city

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')


@api_v1.route('/equipos', methods=['GET'])
def get_equipos():
    logger.info("GET /api/v1/equipos - obteniendo todos los equipos")

    equipos = Equipo.query.all()
    equipos_dto = [EquipoResponseDTO.model_validate(e) for e in equipos]
    response = [e.model_dump() for e in equipos_dto]

    return jsonify(response), 200


@api_v1.route('/equipos/<int:id>', methods=['GET'])
async def get_equipo_by_id(id):
    logger.info(f"GET /api/v1/equipos/{id} - obteniendo equipo por id con clima")

    equipo = Equipo.query.get(id)

    if equipo is None:
        logger.warning(f"Equipo con id {id} no encontrado")
        return jsonify({"error": f"Equipo con id {id} no encontrado"}), 404

    weather_data = await get_weather_by_city(equipo.ciudad)

    equipo_dto = EquipoResponseDTO.model_validate(equipo)
    response = equipo_dto.model_dump()
    response["weather"] = weather_data

    return jsonify(response), 200


@api_v1.route('/equipos', methods=['POST'])
def create_equipo():
    body = request.get_json()
    logger.info(f"POST /api/v1/equipos - creando equipo con body={body}")

    try:
        dto = NewEquipoDTO.model_validate(body)

        nuevo_equipo = Equipo(
            nombre=dto.nombre,
            ciudad=dto.ciudad,
            fundacion=dto.fundacion,
            liga=dto.liga,
            pabellon=dto.pabellon,
            aforo=dto.aforo,
            cantera=dto.cantera,
            user_id=dto.user_id
        )

        db.session.add(nuevo_equipo)
        db.session.commit()

        response_dto = EquipoResponseDTO.model_validate(nuevo_equipo)
        logger.info(f"Equipo creado correctamente con id {nuevo_equipo.id}")

        return jsonify(response_dto.model_dump()), 201

    except ValidationError as e:
        logger.error(f"Error de validación al crear equipo: {e.errors()}")
        return jsonify(e.errors()), 400


@api_v1.route('/equipos/<int:id>', methods=['PUT'])
def update_equipo(id):
    body = request.get_json()
    logger.info(f"PUT /api/v1/equipos/{id} - actualizando equipo con body={body}")

    equipo = Equipo.query.get(id)
    if equipo is None:
        logger.warning(f"Equipo con id {id} no encontrado para actualizar")
        return jsonify({"error": f"Equipo con id {id} no encontrado"}), 404

    try:
        dto = EditEquipoDTO.model_validate(body)
        campos_actualizados = dto.model_dump(exclude_unset=True)

        for field, value in campos_actualizados.items():
            setattr(equipo, field, value)

        db.session.commit()

        response_dto = EquipoResponseDTO.model_validate(equipo)
        logger.info(f"Equipo con id {id} actualizado correctamente")

        return jsonify(response_dto.model_dump()), 200

    except ValidationError as e:
        logger.error(f"Error de validación al actualizar equipo {id}: {e.errors()}")
        return jsonify(e.errors()), 400


@api_v1.route('/equipos/<int:id>', methods=['DELETE'])
def delete_equipo(id):
    logger.info(f"DELETE /api/v1/equipos/{id} - eliminando equipo")

    equipo = Equipo.query.get(id)

    if equipo is None:
        logger.warning(f"Equipo con id {id} no encontrado para eliminar")
        return jsonify({"error": f"Equipo con id {id} no encontrado"}), 404

    db.session.delete(equipo)
    db.session.commit()

    logger.info(f"Equipo con id {id} eliminado correctamente")
    return jsonify({"message": f"Equipo con id {id} eliminado correctamente"}), 200