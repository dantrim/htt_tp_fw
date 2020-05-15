# Contributing to tp-fw

## Pull/Merge Requests

To make the pull/merge request process much smoother we strongly recommend that you setup the git pre-commit
hook for [Black](https://github.com/psf/black) and [flake8](https://github.com/pycqa/flake8/).
See [here](https://ljvmiranda921.github.io/notebook/2018/06/21/precommits-using-black-and-flake8/) for walkthrough
for doing this. Once pre-commit is setup, run

```
pre-commit install
```

This will run `black` and `flake8` over your code each time you attempt to make a commit and warn you if there
is an error, canceling the commit.

### WIP

Unless you are making a single-commit pull/merge request, please create a WIP pull request.
Outline the work that will be done in this ongoing pull request. When you are close to being
done please assigne someone with Approver permissions to follow the pull request.

### Pull/Merge Requests Procedure

If you would like to make a pull/merge request, please:

1. Make a fork of the project
2. Start a pull/merge request to let the project maintainers know you're working on it
3. Commit your changes to a *feature branch* of your fork, and push to your branch
4. Test your changes [WIP]
5. Update your fork to make sure your changes do not conflict with the current state of the master branch
6. Request that your changes be accepted

## Bug Reports

If you have found a bug, please report it by filling out the [bug report template](???)

## Making a pull/merge request

We try to follow [Conventional Commit](https://www.conventionalcommits.org/) for commit messages and
pull/merge request titles.