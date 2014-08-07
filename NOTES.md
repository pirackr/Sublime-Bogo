Workflow for releasing a new version:

1. Update the version in `setup.py` (even the `download_url`). Commit it with message "Bump version to x.x.x"
2. Tag the new commit as vx.x.x (v1.1, v1.0.1)
3. Push to Github
4. Update the releases page: https://github.com/BoGoEngine/bogo-python/releases
5. Upload to PyPI: https://docs.python.org/2/distutils/packageindex.html#package-index