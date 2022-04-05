"""
ENACOM Python bootcamp

API (interface de programação de aplicações)
para resolução de problemas de otimização.
"""
from typing import Union
from fastapi import FastAPI
from http import HTTPStatus
from api.schemas import HealthCheckResponse
from api.schemas import OptimizationInput 
from api.schemas import NotFoundError 
from api.schemas import OptimizationOutput

from api.optimization import problem

from fastapi import Depends
from api.database import Base, engine, SessionLocal

# Create the database
Base.metadata.create_all(engine)

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


api = FastAPI(
    title='ENACOM Python bootcamp API',
    version='0.1.1',
    description=(
        'API (Interface de programação de aplicações)'
        'para resolução de problemas de otimização.'
    ),
)


@api.get(
    '/'
)
def root():
    response = {
        "message": f"{api.title}. versão: {api.version}\n{api.description}"
    }

    return response


@api.get(
    '/healthcheck',
    tags=['healthcheck'],
    summary='Integridade do sistema',
    description='Verifica se o servidor da API está ativo',
    response_model=HealthCheckResponse
)
def healthcheck():
    message = HealthCheckResponse()

    return message


@api.post(
    '/results/{code}',
    summary='Resultado da otimização por código',
    response_model=OptimizationOutput,
    responses={
        HTTPStatus.NOT_FOUND.value: {
            'description': 'Resultado da otimização não encontrado',
            'model': NotFoundError
        }
    }
)
def post_results_code(code: int, optimization_input: OptimizationInput) -> Union[OptimizationOutput, NotFoundError]:
    response = problem.solve(
        optimization_input=optimization_input
    )
    response = OptimizationOutput(
        code=code,
        results=response
    )

    return response


@api.post(
    '/solve',
    summary='Resolver o problema de otimização',
    responses={
        HTTPStatus.NOT_FOUND.value: {
            'description': 'Otimização não resolvida',
            'model': NotFoundError
            }
        }
)
def post_solve(
    optimization_input: OptimizationInput
):
    """
    Resolver problema de otimização
    """
    response = problem.result(
        optimization_input=optimization_input
    )
    

    return response
