## Installation
To install CDIPpy locally, you can either
1. Clone the repository, navigate to the root directory, and run `pip install .` or
2. Without cloning the repository, install from github:
*https: `pip install git+https://github.com/cdipsw/CDIPpy.git`*
*ssh: `pip install git+ssh://github.com/cdipsw/CDIPpy.git`*

{{ under_construction("add test snippet to check installation here") }}

---

## Development
To set up a development copy of CDIPpy, install the project form source using [`uv`](https://docs.astral.sh/uv/):
``` bash
>>> pip install uv
>>> uv sync --extra dev
>>> source .venv/bin/activate
```

This creates a local, virtual environment at `./.venv` and installs a version of CDIPpy along with several additional `dev` dependencies defined in the pyproject.toml file.

---
### Testing
This project uses python's built in `unittest` package. To run all tests:
~~~ bash
>>> python -m unittest discover
~~~
To run with [`coverage`](https://coverage.readthedocs.io/en/latest/):
~~~ bash
>>> coverage run -m unittest discover
~~~
To view the coverage report:
~~~ bash
>>> coverage report
~~~
---

### Contributing
Contributions are welcome and should be merged via pull request on the `main` branch from a forked repository. Before a PR can be merged, it needs to pass the following checks:

* all tests passed
* coverage >= threshhold
* passes [`flake8`](https://flake8.pycqa.org/en/latest/) linter
* there must be at least one reviewer approval
* a CLA must be signed by the contributor, if this is their first commit

If you do not wish you manually check the style for every commit, there is a pre-commit hook that can do it for you. After setting up CDIPpy for development, install the hook with: `pre-commit install`. The installed hook will auto-format the files in your commit with [`black`](https://black.readthedocs.io/en/stable/) and checked for any remaining format errors with `flake8`.
