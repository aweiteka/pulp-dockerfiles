#!/usr/bin/env python

from optparse import OptionParser
import ConfigParser

import os
import sys
import subprocess
import tempfile

class Session(object):
    @property
    def opts(self):
	parser = OptionParser(usage=self.usage, version="%prog 0.1")
	parser.add_option("-i", "--id",
			  action="store",
			  dest="repo_id",
              metavar="REPO",
			  default=False,
			  help="Pulp repository ID, required for most pulp commands. Only alphanumeric, ., -, and _ allowed")
	parser.add_option("-r", "--repo",
			  action="store",
			  dest="registry_id",
              metavar="REGISTRY",
			  default=False,
			  help="Docker registry name for 'docker pull <my/registry>'. If not specified the repo id will be used",)
	parser.add_option("-u", "--url",
			  action="store",
			  dest="redirect_url",
              metavar="URL",
			  default=False,
			  help="The URL that will be used when generating the redirect. Defaults to pulp server, https://<pulp_server>/pulp/docker/<repo_id>",)
	parser.add_option("-f", "--file",
			  action="store",
			  dest="image_file",
              metavar="FILENAME",
			  default=False,
			  help="Full path to image tarball for upload")
	parser.add_option("-n", "--note",
			  action="store",
			  dest="note",
              metavar="KEY=VALUE",
			  default=False,
			  help="Arbitrary key:value pairs")
	parser.add_option("-p", "--publish",
			  action="store_true",
			  dest="publish",
			  default=False,
			  help="Publish repository. May be added to image upload or used alone.",)
	parser.add_option("-P", "--port",
			  action="store",
			  dest="port",
			  default="8080",
			  help="Port for redirect URL where images will be served from. Written to .json file for crane.",)
	parser.add_option("-l", "--list",
			  action="store_true",
			  dest="list_repos",
			  default=False,
			  help="List repositories. Used alone.",)
	(options, args) = parser.parse_args()
        #if len(options) < 1:
        #    parser.print_help()
        #    exit(1)

        # FIXME: option scope not yet determined
        #self.validate_args(parser, options)
        return options

    @property
    def conf_redirect_url(self):
        file = os.path.expanduser('~/.pulp/publish.conf')
	config = ConfigParser.RawConfigParser()
	config.read(file)
        return config.get('redirect', 'url')

    def validate_args(self, parser, options):
        mandatories = ['repo_id']
        for m in mandatories:
            if not options.__dict__[m]:
                parser.error("Required option missing: " + m)

    @property
    def usage(self):
        return """
    Upload (2 methods): will create repo if needed, optional publish
      STDIN from "docker save"
      docker save <docker_repo> | %prog --id <pulp_id> [OPTIONS]

      from previously saved tar file
      %prog --id <pulp_id> -f /run/docker_uploads/<image.tar> [OPTIONS]

    Create repo only (do not upload or publish):
    ./%prog --id <pulp_id> [OPTIONS]

    Publish existing repo:
    ./%prog --id <pulp_id> --publish

    List repos:
    ./%prog --list"""

    @property
    def client_base(self):
        return ["/usr/bin/pulp-admin", "docker", "repo"]

    def is_repo(self, repo):
        return any(repo in r for r in self.repo_list_short)

    @property
    def repo_list_short(self):
        repos = []
        for r in self.check_cmd("list -s").stdout:
            repos.append(r)
        return repos

    @property
    def repo_list_long(self):
        return self.run_cmd("list --fields id,notes,content_unit_counts")

    def modify_url(self, url):
        # http://host:8080/pulp/docker/true
        return url + ":" + self.opts.port + "/pulp/docker/" + self.opts.repo_id

    def create_repo(self):
        if not self.is_repo(self.opts.repo_id):
            options = ""
            if self.opts.redirect_url:
                options += "--redirect-url %s " % self.modify_url(self.opts.redirect_url)
            else:
                options += "--redirect-url %s " % self.modify_url(self.conf_redirect_url)
            if self.opts.registry_id:
                options += "--repo-registry-id %s " % self.opts.registry_id
            if self.opts.note:
                options += "--note %s " % self.opts.note
            self.run_cmd("create --repo-id %s %s" % (self.opts.repo_id, options))
        else:
            print "Repository %s exists. Skipping repo create." % self.opts.repo_id

    def upload_image(self):
        # FIXME: move to validate section
        #if not self.is_stdin and not self.opts.image_file:
        #    print "STDIN or tar file not provided. Skipping upload."
        #    return
        image_tar = ""
        if self.opts.image_file:
            image_tar = self.opts.image_file
        else:
            image_tar = self.stdin_tar_file
        self.run_cmd("uploads upload --repo-id %s -f %s" % (self.opts.repo_id, image_tar))

    def publish_repo(self):
        self.run_cmd("publish run --repo-id %s" % self.opts.repo_id)

    def check_cmd(self, cmd):
        cmd = cmd.split()
        proc = subprocess.Popen(self.client_base + cmd, stdout=subprocess.PIPE)
        proc.wait()
        return proc

    def run_cmd(self, cmd):
        cmd = cmd.split()
        return subprocess.call(self.client_base + cmd)

    @property
    def stdin_tar_file(self):
	CHUNKSIZE = 1048576
        f = tempfile.NamedTemporaryFile(mode='w+b', delete=False)
	sys.stdin = os.fdopen(sys.stdin.fileno(), 'rb', 0)
        print "Saving file from STDIN "
	try:
	    bytes_read = sys.stdin.read(CHUNKSIZE)
	    while bytes_read:
		for b in bytes_read:
		    f.write(b)
		bytes_read = sys.stdin.read(CHUNKSIZE)
	finally:
            print "completed"
	    pass
        return f.name



def main():
    session = Session()
    if session.opts.list_repos:
        session.repo_list_long
        exit(0)
    session.create_repo()
    session.upload_image()
    if session.opts.publish:
        session.publish_repo()

if __name__ == '__main__':
    main()
