Vendor cookbooks
================

Cookbooks under vendor-cookbooks are managed by [berkshelf](http://berkshelf.com/) and will be
provisioned based on the contents of the [Berksfile](../Berksfile) and 
[Berksfile.lock](../Berksfile.lock). They are not directly tracked in this source repository and 
any local changes you make will be lost.

Berkshelf is like composer, bundler, etc - a tool for managing cookbook dependencies and versions. 
Similar to these tools, the lock file tracks a specific version of a cookbook and ensures exactly
that revision is installed on build, QA and production servers.

The workflow is very similar - to add a new cookbook to the project, just add the reference to the 
Berksfile:

    cookbook 'mysql'
    # or to use a custom fork of the community cookbook
    cookbook 'mysql', git://github.com/ingenerator/chef-mysql.git

Then run `vagrant provision` to update your Berksfile.lock, install the new cookbook and re-provision
the local server as required.

To update to the latest version of an existing cookbook:

    # On the vagrant guest over SSH
    cd /vagrant
    berks update mysql

    # On the host
    vagrant provision

The Berksfile.lock should be committed to source control at each point.

For more advanced configuration, version management, etc, see the main Berkshelf documentation.