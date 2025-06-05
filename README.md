# CDIPpy
A python library for navigating and accessing CDIP products.

## In this package
_List of functions, WIP_  
* data access
*

## Installation
To install CDIPpy locally, you can either  
1.  clone the repository, navigate to the root directory, and run `pip install .` or   
2. without cloning the repositorym, install from github: `pip install git+https://github.com/cdipsw/CDIPpy.git`


## Usage
_Directions for use, WIP_

## Development
To set up a development copy of CDIPpy, install the project form source using `uv`:  
``` bash
pip install uv
uv venv
source activate .venv/bin/activate
uv pip install -e .[dev]
```
This creates a local, virtual environment at `./.venv`, and installs a version of CDIPpy that is editable (`-e`), along with several additional dev dependencies (`[dev]`).

### Testing
This project uses python's built in `unittest` package. To run all tests: 
~~~bash
python -m unittest discover
~~~
To run with coverage:
~~~bash
coverage run -m unittest discover
~~~
To view the coverage report:
~~~bash
coverage report
~~~

### Contributing
Contributions are welcome and should be merged via pull request on the `main` branch from a forked repository. Before a PR can be merged, it needs to pass the following checks:

* all tests passed
* coverage >= 90%
* passes `flake8` linter
* there must be at least one reviewer approval
* a CLA must be signed by the contributor, if this is their first commit

If you do not wish you manually check the style for every commit, there is a pre-commit hook that can do it for you. After setting up CDIPpy for development, install the hook with: `pre-commit install`. The installed hook will auto-format the files in your commit with `black` and check for any remaining format errors with `flake8`. 