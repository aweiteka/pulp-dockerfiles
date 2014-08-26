#!/usr/bin/python -Es

"""Docker-focused client for pulp docker registry
"""

import argparse
import os.path
import getpass

class Environment(object):
    def __init__(self):
        self.conf_dir = os.path.expanduser("~") + "/dev/tmp/.pulp"
        self.conf_file = "temp.conf"
        self.user_cert = "user-cert.pem"
        self.uploads_dir = "/run/docker_uploads"

    def setup(self):
        if not self.is_configured:
            print "Registry config file not found. Setting up environment."
            self.create_config()
        if not self.is_loggedin:
            print "User certificate not found."
            self.login_user()
        self.set_context()

    @property
    def is_configured(self):
        return os.path.isfile("%s/%s" % (self.conf_dir, self.conf_file))

    @property
    def is_loggedin(self):
        return os.path.isfile("%s/%s" % (self.conf_dir, self.user_cert))

    def create_config(self):
        print "Creating config file %s/%s" % (self.conf_dir, self.conf_file)
        if not os.path.exists(self.conf_dir):
            os.makedirs(self.conf_dir)
        if not os.path.exists(self.uploads_dir):
            print "Creating %s" % self.uploads_dir
            os.makedirs(self.uploads_dir)

        pulp_hostname = raw_input("Enter registry server hostname: ")
        while pulp_hostname is "":
            pulp_hostname = raw_input("Invalid hostname. Enter registry server hostname, e.g. registry.example.com: ")
        verify_ssl = raw_input("Verify SSL (requires CA-signed certificate) [False]: ") or "False"
        f = open("%s/%s" % (self.conf_dir, self.conf_file), "w")
        f.write("[server]\nhost = %s\nverify_ssl = %s\n" % (pulp_hostname, verify_ssl))
        f.close()

    def set_context(self):
        print "chcon -Rvt svirt_sandbox_file_t %s" % self.conf_dir
        print "sudo chcon -Rv -u system_u -t svirt_sandbox_file_t %s" % self.uploads_dir

    def login_user(self):
        local_user = getpass.getuser()
        username = raw_input("Enter registry username [%s]: " % local_user) or local_user
        while username is "":
            username = raw_input("Invalid username. You must have a registry username to continue. If not known see system administrator: ")
        password = getpass.getpass("Enter registry password: ")
        while password is "":
            password = getpass.getpass("Password blank. Enter registry password: ")
        cmd = "-u %s -p %s" % (username, password)
        c = Command(cmd,"login")
        c.run()

    def logout_user(self):
        cmd = ""
        c = Command(cmd,"logout")
        c.run()

class Command(object):
    def __init__(self,cmd,mode=None):
        self.cmd = cmd
        self.mode = mode
        self.base_cmd = "sudo docker run --rm -t -v ~/.pulp:/.pulp -v /run/docker_uploads/:/run/docker_uploads/ aweiteka/pulp-admin"

    def run(self):
        print "%s %s %s" % (self.base_cmd, self.mode, self.cmd)

    def convert_repo_name(self, repo):
        return repo.replace("/", "-")


def parse_args():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help='sub-command help', dest='mode')
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
    login_parser = subparsers.add_parser('login', help='Login to pulp registry')
    login_parser.add_argument('-u', '--username',
                       metavar='USERNAME',
                       help='Pulp registry username')
    login_parser.add_argument('-p', '--password',
                       metavar='PASSWORD',
                       help='Pulp registry password')
    logout_parser = subparsers.add_parser('logout', help='Log out of the pulp registry')
    pulp_parser = subparsers.add_parser('pulp', help='pulp-admin commands')
    pulp_parser.add_argument('pulp_cmd',
                       metavar='"PULP COMMAND FOO BAR"',
                       help='pulp-admin command string')
    return parser.parse_args()

def main():
    args = parse_args()
    print args
    env = Environment()
    env.setup()
    cmd = args
    c = Command(cmd,args.mode)
    c.run()

if __name__ == '__main__':
    main()

