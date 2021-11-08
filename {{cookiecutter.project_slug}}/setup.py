"""Package setup module."""

from setuptools import find_packages, setup

setup(
    name="{{cookiecutter.project_slug}}",
    version="0.0.0",
    description="{{cookiecutter.project_description}}",
    author="{{cookiecutter.author}}",
    author_email="{{cookiecutter.author_email}}",
    license="GPLv3",
    long_description=open("README.md").read(),
    packages=find_packages(exclude=("tests",)),
    install_requires=[
        {%- if cookiecutter.requirements != "" -%}
        {% for requirement in cookiecutter.requirements.split(',')|sort %}
        '{{ requirement | trim }}',
        {% endfor %}
        {%- endif -%}
    ],
)
