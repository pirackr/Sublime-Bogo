The subdirectory `/bogo` is a subtree that is managed by `git subtree`. It's
original remote is https://github.com/BoGoEngine/bogo-python. It was added
by the following command:

```bash
$ git subtree add -P bogo --squash https://github.com/BoGoEngine/bogo-python.git master
```

To update it:

```bash
git subtree pull -P bogo --squash https://github.com/BoGoEngine/bogo-python.git master
```

To check out an abitrary commit on the subtree, first add its repo as a remote.

```bash
$ git remote add https://github.com/BoGoEngine/bogo-python.git bogo-python
```

Then merge that particular commit from the remote to the subtree (in this
example, we are merge the 10th commit before master):

```bash
$ git subtree merge --P bogo --squash bogo-python/master~10
```
