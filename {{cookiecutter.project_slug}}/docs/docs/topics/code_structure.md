# Code structure

The sources are in `{{cookiecutter.project_slug}}/`. The structure is as
follows:

```text
  +------------+  +---------------+
  | db backend |  | External APIs |
  +------------+  +---------------+
        |                |
+-------|----------------|---+
|       |                |   |
|  +------+  +--------+  |   |
|  | data |  | domain |  |   |
|  +------+  +--------+  |   |
|   |   |        |       |   |
|   |  +-------------------+ |
|   |  |     service       | |
|   |  +-------------------+ |
|   |        |               |
| +-------------+            |
| | entrypoints |            |
| +-------------+            |
|       |                    |
+-------|--------------------+
        |
   +----------+
   | frontend |
   +----------+

```

Each component should only connect with its connected ones. Each component
contains a `__init__.py` file with a docstring explaining the component's
main functionality.

## Components

### Data

This component is responsible for abstracting the data persistence.

#### Database

Abstraction of the local database.

### Domain

`domain` contains the business actors and logic. It has no dependencies,
so that it can be tested alone and the code is as simple and clear as
possible.

### Service

This component obtains data from the `data` or from external APIs
and interacts
with `domain` for validation and applying logic
when called by the `entrypoints` component.

Having this layer decouples the `domain` from the `data` and the
`entrypoints`, which facilitates testing and implementing new functionality.

#### External APIs

Abstraction of external APIs.

### Entrypoints

This component provides access to the package functionality. The main
entrypoint is a HTTP REST API but other entrypoints, such as CLIs, should be
placed here.
