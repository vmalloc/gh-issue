Overview
========

A very simple workflow for maintaining a project with github involves:

1. Browsing for the issue you want to fix
2. Remembering the issue number and copying the issue text
3. Optionally include a line in your changelog for this new feature, involving the copied text from the issue and the issue number
4. Committing your changes with more-or-less the issue text, and appending the issue number (like `some text (#num)`, so that the commit is linked to the issue).
5. Closing the issue in github and pushing your changes.

I don't know about you - but this drove me nuts when repeated again and again.

This is a small utility to do some of the work for you. It relies on [choose](http://tinyrobotsoftware.com/choose/ ) to quickly select the issue you want. Then it commits your change and optionally edits a [releases](https://github.com/bitprophet/releases )-compliant changelog (under `doc/changelog.rst` currently) to reflect your change. It also prompts you if you want to close the issue at hand automatically.

All you need to do is run:

	$ gh-issue commit

And you're done.
																																																			  
																	 

Licence
=======

BSD3

