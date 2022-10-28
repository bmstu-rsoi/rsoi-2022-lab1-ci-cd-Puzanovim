import os

import uvicorn
from fastapi import FastAPI, status, Request, Response
from fastapi.responses import JSONResponse

from app.db import engine
from app.persons.models import Base
from app.exceptions import NotFoundPerson
from app.persons.routers import router as person_router


app = FastAPI()
app.include_router(person_router, prefix='/api/v1/persons', tags=['Person REST API operations'])


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.exception_handler(NotFoundPerson)
async def not_found_handler(request: Request, exc: NotFoundPerson) -> Response:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={'message': f'Person not found: {exc}'},
    )


if __name__ == "__main__":
    port = os.environ.get('PORT')
    if port is None:
        port = 8080

    uvicorn.run(app, host="0.0.0.0", port=int(port))
