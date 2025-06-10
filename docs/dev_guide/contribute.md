# Contributors guide
Thank you for considering making a contribution to CDIPpy! We welcome all types on contributions, including:

- **new features**: do you have a cool workflow or product that uses CDIP? We'd love to see it!
- **bug fixes**: have you found something that doesn't work? We'd love help fixing it!
- **code cleanup**: some of this code is *really old*; if you have ideas for making if cleaner or more efficient, we want to hear them!
- **documentation and examples**: we would love more examples of `cdippy` library usage

## Setting up your git workflow
This project uses a fork-and-contribute workflow. You will need to make your [fork](https://github.com/cdipsw/CDIPpy/fork) of the repository to work in, and submit changes to CDIPpy via pull request. To set up your workflow, follow these instructions:

1. Fork the respository at [https://github.com/cdipsw/CDIPpy/fork](https://github.com/cdipsw/CDIPpy/fork)
2. Clone the repository from  your fork `git clone https://github.com/{your_github_username}/CDIPpy.git` - this will add your own fork as your `origin` remote repo. *Note: If you already have the main fork cloned, skip to the next step and follow instuctions to add your fork as another remote.*
3. Add the main fork as another remote (or your fork, if you cloned from the main fork). This will allow you to pull latest code from the main fork, but push your own development to your own fork:  
```bash
git add remote cdip https://github.com/{your_github_username}/CDIPpy.git
git fetch cdip
git remote -v
```
If this worked, the last command will show your fork as `origin` and CDIP's as `cdip` (or whatever you have named them, respectively).

## Making your changes


### linting

### testing

### documenting

## Making your pull request
Once you are satisfied with your changes (or just ready to get more eyes on them), open a pull request at: [https://github.com/cdipsw/CDIPpy/pulls](https://github.com/cdipsw/CDIPpy/pulls).


## Get help
If you have an idea but aren't sure how to implement it or would like others to weigh in, open an issue on GitHub at [https://github.com/cdipsw/CDIPpy/issues](https://github.com/cdipsw/CDIPpy/issues)!
