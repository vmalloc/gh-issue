#!/usr/bin/env python
from __future__ import print_function

import os
import subprocess
import sys
import tempfile
from cStringIO import StringIO
from getpass import getpass

import logbook

import click
from github3 import authorize, login


@click.group()
@click.option("-v", "--verbose", count=True)
@click.option("-q", "--quiet", count=True)
def main(verbose, quiet):
    with logbook.NullHandler(), logbook.StreamHandler(sys.stderr, level=logbook.WARNING - verbose + quiet, bubble=False):
        pass


@main.command()
@click.option('--close-issue/--no-close-issue', default=None)
def commit(close_issue):
    issues = list(_get_github_client().iter_issues(sort='updated'))
    p = subprocess.Popen(
        'choose', stdin=subprocess.PIPE, shell=True, stdout=subprocess.PIPE)
    p.stdin.write(_format_issues(issues))
    p.stdin.close()
    if p.wait() != 0:
        raise click.Abort('Could not choose issue')
    text = p.stdout.read().strip()
    issue_index, issue_text = text.split('.', 1)
    issue = issues[int(issue_index)]
    temp_filename = tempfile.mktemp()
    with open(temp_filename, "w") as temp_file:
        temp_file.write(issue_text)
    p = subprocess.Popen(
        "git commit -a -e -F {}".format(temp_filename), shell=True)
    if p.wait() != 0:
        click.echo('Failed to commit changes')
        raise click.Abort()

    if close_issue is None:
        close_issue = click.confirm('Would you like to close the issue?')

    if close_issue:
        issue.close()


def _format_issues(issues):
    returned = ""
    for index, issue in enumerate(issues):
        returned += '{0}. {1} (#{2})\n'.format(index,
                                               issue.title, issue.number)
    return returned


def _get_github_client(credentials_file=os.path.expanduser('~/.gh-issue')):
    if not os.path.exists(credentials_file):

        user = raw_input('Enter github username: ').strip()
        password = getpass('Password for {0}: '.format(user))

        auth = authorize(
            user, password, ['user', 'repo'], 'gh-issue', 'https://github.com/vmalloc/gh-issue', two_factor_callback=_read_two_factor_auth)

        logbook.debug('Got auth: {} ({})', auth.id, auth.token)

        with open(credentials_file, 'w') as fd:
            print(auth.token, file=fd)
            print(auth.id, file=fd)
        gh = login(token=auth.token)
    else:
        token = id = ''
        with open(credentials_file) as fd:
            token = fd.readline().strip()
            id = int(fd.readline().strip())
        gh = login(token=token)
        #auth = gh.authorization(id)
        #auth.update(add_scopes=['repo:status', 'gist'], rm_scopes=['user'])

    return gh


def _read_two_factor_auth():
    return raw_input('Enter Github 2-Factor Auth code: ').strip()


if __name__ == "__main__":
    main()
