# Basic Changelog Generator
This action parses all the commits between the latest two tags of your git repository and generates a changelog according to the provided configuration file.

Usage:
```yaml
on: [push]

jobs: 
  self-use-action:
    runs-on: ubuntu-latest
    name: Generate the changelog
    steps:
      - name: Checkout
        uses: actions/checkout@v3
        with:
          fetch-depth: '0' # Make sure to fetch all your history otherwise the tags wont't be available.
      - name: Generate changelog
        id: get_changelog
        uses: massicer/basic-changelog-generator@1.0.0
      - name: Print the changelog
        run: echo "${{ steps.get_changelog.outputs.changelog }}"
```