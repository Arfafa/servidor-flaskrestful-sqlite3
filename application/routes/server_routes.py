from flask import request
from flask_restful import Resource
from application.server import api
from application.database.utils import get_database
from application.routes.utils import get_json, get_from_request
from application.routes.utils import HTTP_STATUS_CODE


class Estudante(Resource):
    def get(self):
        database = get_database()

        return database.listar_estudantes(), HTTP_STATUS_CODE['OK']

    def post(self):
        try:
            data = get_json(request)

            database = get_database()
            resp = database.inserir_estudante(data)

        except Exception as e:
            resp = {'msg': str(e)}

            return resp, HTTP_STATUS_CODE['BAD_REQUEST']

        return resp, HTTP_STATUS_CODE['OK']

    def put(self):
        try:
            data = get_json(request)

            database = get_database()
            resp = database.alterar_estudante(data)

        except Exception as e:
            resp = {'msg': str(e)}

            return resp, HTTP_STATUS_CODE['BAD_REQUEST']

        return resp, HTTP_STATUS_CODE['OK']

    def delete(self):
        try:
            data = get_json(request)
            estudante_id = get_from_request(data, 'id')

            database = get_database()
            resp = database.deletar_estudante(estudante_id)

        except Exception as e:
            resp = {'msg': str(e)}

            return resp, HTTP_STATUS_CODE['BAD_REQUEST']

        return resp, HTTP_STATUS_CODE['OK']


class EstudanteFiltro(Resource):
    def post(self):
        try:
            data = get_json(request)

            database = get_database()
            resp = database.filtrar_estudantes(data)

        except Exception as e:
            resp = {'msg': str(e)}

            return resp, HTTP_STATUS_CODE['BAD_REQUEST']

        return resp, HTTP_STATUS_CODE['OK']


def init_routes():
    api.add_resource(Estudante, '/estudante')
    api.add_resource(EstudanteFiltro, '/estudante/filtro')
