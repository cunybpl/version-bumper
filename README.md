# version-bumper
Provides a poetry plugin to allow for easy version bumping.

## Installation
To install the version bumper plugin run the following command in a shell:
`poetry self add git+ssh://git@github.com:cunybpl/version-bumper`

Once run, the command will be available everywhere on your local system.

To remove:
`poetry self remove version-bumper`

## Usage
`poetry bumpversion [options] <major|minor|patch|prerelease> <module-name>`

With the options being:
- --tag (-t): create a new tag in git
- --push (-p): push this new tag to `origin`
- --dry-run (-d): only display the changes to be made, but do not make them
