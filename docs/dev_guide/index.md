# Installing CDIPpy for development
This page contains instructions for CDIPpy users interested in customizing or contributing to the library.

## Download source
Clone the [CDIPpy repository](https://github.com/cdipsw/CDIPpy):

* using `ssh` - `git clone git@github.com:cdipsw/CDIPpy.git`
* using `https` - `git clone https://github.com/cdipsw/CDIPpy.git`

If you need help getting started with [Git](https://git-scm.com/doc) and [GitHub](https://docs.github.com/en/enterprise-cloud@latest/get-started).
You'll specifically want to look at configuring credentials with [https](https://git-scm.com/docs/gitcredentials) or [ssh](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).

[Dangit, Git!?!](https://dangitgit.com/) is another great resource for fixing git problems.

## Install with dev tools
It is recommended to us [`uv`](https://docs.astral.sh/uv/) to manage you development environment for this project, but other package managers will likely work as well. This documentation provides instructions for using `uv`.

Navigate to the project root dirctory ('CDIPpy/') and run the following:
``` bash
>>> pip install uv # install uv pacakge manager
>>> uv sync --extra dev # create a virtual envionment at CDIPpy/.venv/, install the source code, its runtime dependencies and it's dev dependencies defined in pyproject.toml.
>>> source .venv/bin/activate # activate the environment
```
The `--extra dev` specifier installs the packages requires to run tests, lint, and build documentation.

### testing
You can check that your dev installation was successful by running unit tests from the root directory: `python -m unittest discover`.
This runs every test in the library; you should see all successful tests.

Learn more about running specific tests or subsets from the [`unittest` docs](https://docs.python.org/3/library/unittest.html).

### linting
This library uses `flake8` to check for adherance to the [PEP8](https://peps.python.org/pep-0008/) style guide. To check whether your code is compliant with the project style, run `flake8 .` from the project root.  You can fix problems manually, or use a tool like [`black`](https://black.readthedocs.io/en/stable/) to autolint: `black .`.

This project also provides a [`pre-commit`](https://pre-commit.com/) hook to manage style for you autmatically on every `git commit`. To install it, run `pre-commit install` from the project root - this will use `black` and `flake` to autolint and check any changes you make for style before committing them to the repository.
