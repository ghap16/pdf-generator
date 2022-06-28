# pdf-generator
Service to generate a pdf from an HTML template


## Requirements

python == 3.9
poetry >= 1.2.0

## Steps to run the project

### Initialize environment

```
$ poetry shell
```
or
```
$ make venv
```

### Install dependencies

```
$ poetry install
```
or
```
$ make install
```

### Run project

```
$ uvicorn src.main:app
```
or
```
$ make run
```

## Extras

### Formatting

```
$ isort
$ black
```
or
```
$ make fmt
```

### Lint
```
$ isort --check-only
$ black --check
$ flake8
```
or
```
$ make lint
```
