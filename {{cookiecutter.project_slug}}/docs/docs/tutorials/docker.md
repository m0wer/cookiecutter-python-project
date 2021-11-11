# Docker

This project can executed with `docker`.

## Building

To build the Docker image run
(from the root directory of this repository):

```bash
docker build -t local/{{cookiecutter.project_slug_hyphen}} .
```

## Running

Then, to run it:

```bash
docker run \
    --rm \
    --name {{cookiecutter.project_slug_hyphen}} \
    -p 8000:8000 \
    -e ENV_VAR=value \
    -it \
     local/{{cookiecutter.project_slug_hyphen}}
```

*For the list of required environment variables check
[Getting started](getting_started.md).*

You can then access the HTTP API at <http://localhost:8000>.

If `WEB_CONCURRENCY` is not set, the number of workers will be two times
the number of CPU cores/threads.

The environment variables from
[tiangolo/uvicorn-gunicorn-fastapi](https://hub.docker.com/r/tiangolo/uvicorn-gunicorn-fastapi)
are also supported.
