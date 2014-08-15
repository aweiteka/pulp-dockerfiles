#!/usr/bin/python -Es

"""Admin pulp as a docker registry

sudo ./registry_admin.py
    login # prompt for user/pass if no .pulp/admin.conf
    create my/app
    list repos
    list images my/app
    push my/app
    pulp <native_pulp_cmds>
"""

import argparse

class Cli(object):
    @property
    def args(self):
        parser = argparse.ArgumentParser()

        subparsers = parser.add_subparsers(help='sub-command help')
        push_parser = subparsers.add_parser('push', help='repository')
        push_parser.add_argument('repo',
                           metavar='MY/APP',
                           help='Repository name')
        create_parser = subparsers.add_parser('create', help='repository')
        create_parser.add_argument('repo',
                           metavar='MY/APP',
                           help='Repository name')
        create_parser.add_argument('-g', '--git-url',
                           metavar='http://git.example.com/repo/myapp',
                           help='URL of git repository for Dockerfile')
        create_parser.add_argument('-t', '--git-tag',
                           metavar='TAG',
                           help='git tag name for Dockerfile repository')
        create_parser.add_argument('-b', '--git-branch',
                           metavar='BRANCH',
                           help='git branch name for Dockerfile repository')
        list_parser = subparsers.add_parser('list', help='images or repos')
        list_parser.add_argument('list_item',
                           metavar='repos|images',
                           choices=['repos', 'images'],
                           help='What to list')
        login_parser = subparsers.add_parser('login', help='Login to pulp server')
        login_parser.add_argument('username',
                           metavar='USERNAME',
                           help='Pulp registry username')
        pulp_parser = subparsers.add_parser('pulp', help='pulp-admin commands')
        pulp_parser.add_argument('pulp_cmd',
                           metavar='"PULP COMMAND FOO BAR"',
                           help='pulp-admin command string')
        return parser.parse_args()

    def convert_repo_name(self):
        print self.args


def main():
    cli = Cli()
    cli.convert_repo_name()

if __name__ == '__main__':
    main()

