# Contributors guide
Thank you for considering making a contribution to CDIPpy! We welcome all types of contributions, including:

- **new features**: do you have a cool workflow or product that uses CDIP? We'd love to see it!
- **bug fixes**: have you found something that doesn't work? We'd love help fixing it!
- **code cleanup**: some of this code is *really old*; if you have ideas for making if cleaner or more efficient, we want to hear them!
- **documentation and examples**: we would love more examples of `cdippy` library usage

## Setting up your git workflow
This project uses a fork-and-pull-request workflow. You will need to make your [fork](https://github.com/cdipsw/CDIPpy/fork) of the repository to work in, and submit changes to CDIPpy via pull request. To set up your workflow, follow these instructions:

1. Fork the repository at [https://github.com/cdipsw/CDIPpy/fork](https://github.com/cdipsw/CDIPpy/fork)
2. Clone the repository from  your fork `git clone https://github.com/{your_github_username}/CDIPpy.git` - this will add your own fork as your `origin` remote repo. *Note: If you already have the main fork cloned, skip to the next step and follow instructions to add your fork as another remote.*
3. Add the main fork as another remote (or your fork, if you cloned from the main fork). This will allow you to pull latest code from the main fork, but push your own development to your own fork:  
```bash
git add remote cdip https://github.com/cdipsw/CDIPpy.git
git fetch cdip
git remote -v
```
If this worked, the last command will show your fork as `origin` and CDIP's as `cdip` (or whatever you have named them, respectively).

## Making your changes
Before starting to develop, make sure you're working from the latest commit:
```bash
git checkout main # make sure this is cdip/main not your fork
git pull
git checkout -b example-branch
```
This will create a new branch called `example-branch` based on the latest commit to `main`. Now you can start making your changes.  

Any changes you plan to contribute should be sure to follow the project's style guide, testing structure, and be up-to-date with documentation.

### linting
First you'll need to make sure your code style matches the rest of `cdippy` by using the `flake8` linter to check for adherence to the [PEP8](https://peps.python.org/pep-0008/) style guide:  
```bash
flake8 .
```
If this command is successful, your style is up to date! Otherwise, the output will indicate where in the project the style is not compliant. You can manually fix these style deviations, or use  a tool like [`black`](https://black.readthedocs.io/en/stable/) to autolint: 
```bash
black .  
```

This project also provides a [`pre-commit`](https://pre-commit.com/) hook to manage style for you automatically on every `git commit`. From  the project root:
```bash
pre-commit install
```
When you run `git commit` from your repo with the pre-commit hook installed, `black` will attempt to autolint the code and `flake8` will verify the results; the commit will fail if style errors are found, and you will need to manually fix them and try to commit again.   

### testing
With very few exceptions, every change should be tested! Your contribution cannot be accepted with failing tests or with large volumes of untested code. This project uses [`unittest`](https://docs.python.org/3/library/unittest.html) and [`coverage`](https://coverage.readthedocs.io/en/7.8.2/) to check that the code is thoroughly tets.

Make sure all tests pass by running `python -m unittest discover` from the project root.   
Learn more about running specific tests or subsets from the [`unittest` docs](https://docs.python.org/3/library/unittest.html).

Make sure test coverage is high by running `coverage run -m unittest discover`, which will run all tests and generate a file called `.coverage`. When tests have complete, run `coverage report`. The output of `report` will show what percentage of the code base was executed by the test suite - higher coverage means a more reliable library!

Learn more about interpreting coverage reports from the [docs](https://coverage.readthedocs.io/en/7.8.2/).


### documenting
Some contributions may require edits to the documentation,such as: new features, documentation for previously undocumented features, or changes to end behavior. This project uses [`mkdocs`](https://www.mkdocs.org/) to build a static site which is hosted on [GitHub pages](https://docs.github.com/en/pages). Before creating a pull request, be sure make any necessary changes to the documentation.

---
**1) Edit a page**
Make edits to the `.md` file under ['/docs/'](https://github.com/cdipsw/CDIPpy/tree/main/docs) which corresponds to the page you're editing

---
**2) Make a new page or section**
To add new pages to navigation, you'll need to create a new `.md` file in  `/docs/` and edit [`mkdocs.yml`](https://github.com/cdipsw/CDIPpy/blob/main/mkdocs.yml) to include it.

For example:  
Create a new folder called "my_changes" and a file called "mychanges/change_1.md" under '/docs'.  
Add it to the `nav` tag of `mkdocs.yml`:

```yml
nav:
  - Home: index.md
  - Quick start: quickstart.md
  ...
  - My changes:
    - First change: my_changes/change_1.md
``` 

---
**3) Preview your changes**
You can preview your changes locally by running `mkdocs serve` and going to [http://localhost:8000/](http://localhost:8000/).

---
**4) Using and building site macros**
Reusable site4 macros are defined in `./main.py`. The current list of supported macros are:

- Under construction banner: 
```html
/* remove spaces between curly braces */
{ { under_construction("Your text here") } }
```
{{ under_construction("Your text here") }}

---
**4) Publish your changes**
Publishing the updated documentation to the live site will be handled for you automatically by GitHub! If you're interested in how it works, read on, otherwise, skip to the next section.

How publishing works:

1. When you open a pull request with changes to either `mkdocs.yml` or the `/docs/` directory, [this workflow](https://github.com/cdipsw/CDIPpy/blob/main/.github/workflows/docs.yml) will be triggered and will build the static site (html) and push it to a branch called `gh-pages`.
2. If the build is successful, a new job will run which will serve the new source in `gh-pages`. 
3. You can view running and completed workflows [here](https://github.com/cdipsw/CDIPpy/actions).


---

####

## Making your pull request
Once you are satisfied with your changes (or just ready to get more eyes on them), open a pull request at: [https://github.com/cdipsw/CDIPpy/pulls](https://github.com/cdipsw/CDIPpy/pulls).

Step 1: open the pull request
    a. select 'New pull request'
    b. make sure the `base` branch is `cdipsw/CDIPpy/main`
    c. choose a branch to compare - make sure you have selected "compare across forks" so that you can choose branches from your own fork
    d. Click "Create pull request". 
Step 2: edit the pull request
    a. give your PR a descriptive title
    b. tag any issues your PR resolves
    c. provide a description with an overview of your changes and any details a reviewer might need to know.
    d. verify that your changes look correct
    e. Click "Create pull request"
Step 3: meet merge criteria - the next step is to see if the PR build passes. Checks will should up on your PR page with a status (Not started, passed, failed, canceled, etc.)
    a. all tests must pass
    b. test coverage must meet the threshold
    c. contributors must sign a CLA
    d. one reviewer must approve the PR - optionally, you can request reviews from specific users from the top right of your PR page under "Reviewers". 

Once all status checks have turned green, the "merge" button will be enabled and the code can be merged into the `main` branch. Congrats, you've made a contribution!

## Get help
If you have an idea but aren't sure how to implement it or would like others to weigh in, open an issue on GitHub at [https://github.com/cdipsw/CDIPpy/issues](https://github.com/cdipsw/CDIPpy/issues)!
