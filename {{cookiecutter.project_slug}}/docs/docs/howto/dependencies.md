# Dependencies

The dependencies are fixed to an specific version two ensure
compatibility. The necessary dependencies for running the project
are in `requirements.txt`, and the required
for development purposes (testing, dependency management…) are in
`requirements-dev.txt`.

This files are generated automatically using
[pip-tools](https://github.com/jazzband/pip-tools). `requirements.txt`
is generated from the dependencies specified in `setup.py` (which aren't
fixed to a particular version unless necessary).
`requirements-dev.txt` are generated
from the dependencies specified in `requirements-dev.in` (which aren't fixed
to a particular version) and considering `requirements.txt` and
`docs/requirements.txt` (for compatible versions).

The docs dependencies are fixed to an specific version in
`docs/requirements.txt` which is generated from `docs/requirements.in`.

## Updating the dependencies

**Only run this command in a virtual environment.**

```bash
make update
```

This will update the requirements files and sync the local
virtual environment with them. This will remove extra dependencies
and ensure that the installed ones match the specified versions.
