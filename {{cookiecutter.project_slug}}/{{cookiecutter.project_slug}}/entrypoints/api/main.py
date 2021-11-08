"""Main API."""

from os import environ

from fastapi import FastAPI

DESCRIPTION = "{{cookiecutter.project_description}}"

api = FastAPI(
    name="{{cookiecutter.project_name}}",
    title="{{cookiecutter.project_name}}",
    description=DESCRIPTION,
    root_path=environ.get("ROOT_PATH", ""),
    responses={
        200: {
            "description": "Successful response.",
        },
        400: {"description": "Invalid value for parameter."},
        404: {"description": "No data available."},
    },
    version="0.0.0",
)
