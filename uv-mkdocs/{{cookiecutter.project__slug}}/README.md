# {{cookiecutter.project__name}}

## Setup

1. Install [direnv](https://direnv.net/docs/installation.html)
2. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
3. Run `uv venv` to create virtual env
4. Run `cp .envrc.example .envrc`
5. Run `direnv allow`
6. Run `uv sync`

### Ubuntu dependencies

```shell
sudo apt-get install -y libxcb-cursor-dev
```

## Documentation

```shell
mkdocs build
mkdocs serve
```

[PyQT6 Tutorial](https://www.pythonguis.com/tutorials/pyqt6-widgets/)
