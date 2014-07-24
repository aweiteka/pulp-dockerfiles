#!/usr/bin/env python

from optparse import OptionParser
import os
import sys
import subprocess
import tempfile

class Session(object):
    @property
    def opts(self):
	parser = OptionParser(usage=self.usage, version="%prog 0.1")
	parser.add_option("-r", "--repo",
			  action="store",
			  dest="repo_id",
                          metavar="REPO",
			  default=False,
			  help="Pulp repository ID, required for most pulp commands. Only alphanumeric, ., -, and _ allowed")
	parser.add_option("-R", "--registry",
			  action="store",
			  dest="registry_id",
                          metavar="REGISTRY",
			  default=False,
			  help="Docker registry name for 'docker pull <my/registry>'. If not specified the repo id will be used",)
	parser.add_option("-d", "--description",
			  action="store",
			  dest="repo_description",
                          metavar="DESCRIPTION",
			  default=False,
			  help="Pulp repository description",)
	parser.add_option("-n", "--name",
			  action="store",
			  dest="repo_name",
                          metavar="DISPLAY_NAME",
			  default=False,
			  help="Pulp repository display name",)
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
	parser.add_option("-p", "--publish",
			  action="store_true",
			  dest="publish",
			  default=False,
			  help="Publish repository. May be added to image upload or used alone.",)
	parser.add_option("-l", "--list",
			  action="store_true",
			  dest="list_repos",
			  default=False,
			  help="List repositories. Used alone.",)
	parser.add_option("-D", "--delete",
			  action="store_true",
			  dest="delete_repo",
			  default=False,
			  help="Delete a repository. Used alone.",)
	(options, args) = parser.parse_args()
        #if len(args) < 1:
        #    parser.error("At least one argument is required.")

        # FIXME: option scope not yet determined
        #self.validate_args(parser, options)
        return options

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
      docker save <repo> | ./%prog --repo <repo> [OPTIONS]

      from previously saved tar file
      ./%prog --repo <repo> -f </full/path/to/image.tar> [OPTIONS]

    Create repo only (do not upload or publish):
    ./%prog --repo <repo> [OPTIONS]

    Publish existing repo:
    ./%prog --repo <repo> --publish

    List repos:
    ./%prog --list

    Delete repo and all images:
    ./%prog --repo <repo> --delete"""

    @property
    def client_base(self):
        return ["/usr/bin/pulp-admin", "docker", "repo"]

    def is_repo(self, repo):
        return any(repo in r for r in self.repo_list_short)

    @property
    def is_stdin(self):
        if not sys.stdin.isatty():
            return True
        else:
            return False

    @property
    def repo_list_short(self):
        repos = []
        for r in self.check_cmd("list -s").stdout:
            repos.append(r)
        return repos

    @property
    def repo_list_long(self):
        return self.run_cmd("list --fields id,description,notes,content_unit_counts")

    @property
    def delete_repo(self):
        return self.run_cmd("delete --repo-id %s" % self.opts.repo_id)

    def create_repo(self):
        if not self.is_repo(self.opts.repo_id):
            options = ""
            if self.opts.registry_id:
                options += "--repo-registry-id \"%s\" " % self.opts.registry_id
            if self.opts.repo_description:
                options += "--description \"%s\" " % self.opts.repo_description
            if self.opts.repo_name:
                options += "--display-name \"%s\" " % self.opts.repo_name
            if self.opts.redirect_url:
                options += "--redirect-url %s " % self.opts.redirect_url
            print "create --repo-id %s %s" % (self.opts.repo_id, options)
            self.run_cmd("create --repo-id %s %s" % (self.opts.repo_id, options))
        else:
            print "Repository %s exists. Skipping repo create." % self.opts.repo_id

    def upload_image(self):
        # FIXME: move to validate section
        if not self.is_stdin and not self.opts.image_file:
            print "STDIN or tar file not provided. Skipping upload."
            return
        image_tar = ""
        if self.is_stdin:
            image_tar = self.save_file()
        else:
            image_tar = self.opts.image_file
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

    def save_file(self):
	CHUNKSIZE = 8192
	tarball = "/tmp/test.tar"
	f = open(tarball, 'wb')
        #f = tempfile.NamedTemporaryFile(mode='w+b')
	sys.stdin = os.fdopen(sys.stdin.fileno(), 'rb', 0)
	try:
	    bytes_read = sys.stdin.read(CHUNKSIZE)
	    while bytes_read:
		for b in bytes_read:
		    f.write(b)
		bytes_read = sys.stdin.read(CHUNKSIZE)
	finally:
	    pass
	#f.close()
        #return f.name
        return tarball



def main():
    session = Session()
    if session.opts.list_repos:
        session.repo_list_long
        exit(0)
    elif session.opts.delete_repo:
        session.delete_repo
        exit(0)
    session.create_repo()
    session.upload_image()
    if session.opts.publish:
        session.publish_repo()

if __name__ == '__main__':
    main()
