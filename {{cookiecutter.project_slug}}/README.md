# {{cookiecutter.project_name}}

[![Actions Status](
{{ cookiecutter.repo_url }}/workflows/main/badge.svg
)]({{ cookiecutter.repo_url }}/actions)
[![pre-commit](
https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
)](https://github.com/pre-commit/pre-commit)

## Installation

Run `pip install .`.

## Development

Run `make install` to install all development dependencies.

## Documentation

You can access the online version at <{{ cookiecutter.docs_url }}>.

Alternatively, after `make install`, to render the documentation run:

```bash
pip install -r requirements.txt
mkdocs serve
```

You can now access the docs at <http://localhost:8000>.
