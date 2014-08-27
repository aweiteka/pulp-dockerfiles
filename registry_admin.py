#!/usr/bin/python -Es

"""Docker-focused client for pulp docker registry
"""

import argparse
import os.path
import subprocess
import getpass
import re

class Environment(object):
    """Host environment"""

    def __init__(self):
        """Environment defaults"""
        self.conf_dir = os.path.expanduser("~") + "/.pulp"
        self.conf_file = "admin.conf"
        self.user_cert = "user-cert.pem"
        self.uploads_dir = "/run/docker_uploads"

    def setup(self):
        """Setup host environment directories and login if needed"""
        if not self.is_configured:
            print "Registry config file not found. Setting up environment."
            self.create_config()
        self.set_context()
        if not self.is_loggedin:
            print "User certificate not found."
            self.login_user()

    @property
    def is_configured(self):
        """Does the pulp configuration file exist?"""
        return os.path.isfile("%s/%s" % (self.conf_dir, self.conf_file))

    @property
    def is_loggedin(self):
        """Does the pulp user certificate exist?"""
        return os.path.isfile("%s/%s" % (self.conf_dir, self.user_cert))

    def create_config(self):
        """Create config dir, uploads dir and conf file"""
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
        """Set SELinux context for dirs"""
        c1 = "sudo chcon -Rvt svirt_sandbox_file_t %s" % self.conf_dir
        proc = subprocess.Popen(c1.split(), stdout=subprocess.PIPE)
        proc.wait()
        c2 = "sudo chcon -Rv -u system_u -t svirt_sandbox_file_t %s" % self.uploads_dir
        proc = subprocess.Popen(c2.split(), stdout=subprocess.PIPE)
        proc.wait()

    def login_user(self):
        """Prompt user to login"""
        local_user = getpass.getuser()
        username = raw_input("Enter registry username [%s]: " % local_user) or local_user
        while username is "":
            username = raw_input("Invalid username. You must have a registry username to continue. If not known see system administrator: ")
        password = getpass.getpass("Enter registry password: ")
        while password is "":
            password = getpass.getpass("Password blank. Enter registry password: ")
        cmd = "login -u %s -p %s" % (username, password)
        c = Command(cmd)
        c.run(stdout=True)

    def logout_user(self):
        """Logout user"""
        cmd = "logout"
        c = Command(cmd)
        c.run(stdout=True)

class Pulp(object):
    """Construct pulp commands"""
    def __init__(self, args):
        self.args = args

    def parsed_args(self):
        """Logic to parse arguments"""
        if self.args.mode in "create":
            return ["docker repo create --repo-id %s" % self.repo_name(self.args.repo)]
        elif self.args.mode in "delete":
            return ["docker repo delete --repo-id %s" % self.repo_name(self.args.repo)]
        elif self.args.mode in "push":
            return ["docker repo create --repo-id %s" % self.repo_name(self.args.repo),
                    "docker repo upload uploads --repo-id %s" % self.repo_name(self.args.repo),
                    "docker repo publish run --repo-id %s" % self.repo_name(self.args.repo)]
        elif self.args.mode in "list":
            if self.args.list_item not in "repos":
                return ["docker repo images -d --repo-id %s" % self.repo_name(self.args.list_item)]
            else:
                return ["docker repo list --details"]

    def repo_name(self, repo):
        """Returns pulp-friendly repository name without slash"""
        return repo.replace("/", "-")

    def execute(self):
        """Send parsed command to command class"""
        for cmd in self.parsed_args():
            c = Command(cmd)
            self.format_output(c.run())

    def format_output(self, output):
        """Format output of commands"""
        if self.args.mode in "list":
            if self.args.list_item in "repos":
                regex = re.compile(r'repo-registry-id:(.+$)', re.I)
            else:
                regex = re.compile(r'image id:(.+$)', re.I)
            for out in output.stdout:
                line = regex.search(out)
                if line:
                    print line.group(1).strip()
        else:
            for out in output.stdout:
                print out.strip()


class Command(object):
    """Build and run command"""
    def __init__(self, cmd):
        self.cmd = cmd

    @property
    def base_cmd(self):
        """Construct base pulp admin container command"""
        env = Environment()
        conf_dir = env.conf_dir
        uploads_dir = env.uploads_dir
        return "sudo docker run --rm -t -v %(conf_dir)s:/.pulp -v %(uploads_dir)s:%(uploads_dir)s aweiteka/pulp-admin" % vars()

    def run(self, stdout=None):
        """Run command"""
        cmd = "%s %s" % (self.base_cmd, self.cmd)
        cmd = cmd.split()
        if stdout:
            subprocess.call(cmd)
        else:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            proc.wait()
            return proc


def parse_args():
    """Parse arguments"""
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
    list_parser = subparsers.add_parser('list', help='repos or images')
    list_parser.add_argument('list_item',
                       metavar='repos|MY/APP',
                       help='Repos or repo images')
    login_parser = subparsers.add_parser('login', help='Login to pulp registry')
    login_parser.add_argument('-u', '--username',
                       metavar='USERNAME',
                       help='Pulp registry username')
    login_parser.add_argument('-p', '--password',
                       metavar='PASSWORD',
                       help='Pulp registry password')
    delete_parser = subparsers.add_parser('delete', help='repository')
    delete_parser.add_argument('repo',
                       metavar='MY/APP',
                       help='Repository name')
    subparsers.add_parser('logout', help='Log out of the pulp registry')
    pulp_parser = subparsers.add_parser('pulp', help='pulp-admin commands')
    pulp_parser.add_argument('pulp_cmd',
                       metavar='"PULP COMMAND FOO BAR"',
                       help='pulp-admin command string')
    return parser.parse_args()

def main():
    """Entrypoint for script"""
    args = parse_args()
    env = Environment()
    if args.mode in "logout":
        env.logout_user()
        exit(0)
    env.setup()
    if args.mode in "login":
        exit(0)
    p = Pulp(args)
    p.execute()

if __name__ == '__main__':
    main()

