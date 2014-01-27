# Install and build wiringpi

# Ensure deploy dirs exist
%w(releases shared).each do | path |
  directory "/var/lib/wiringPi/#{path}" do
    recursive true
    owner    "pi"
    group    "pi"
    mode      0755
  end
end

# Define the build resource
execute "/var/lib/wiringPi/current/build" do
  user   "pi"
  group  "pi"
  action :nothing
end

# Clone and checkout, trigger build if required
deploy "/var/lib/wiringPi" do
  repo     "git://git.drogon.net/wiringPi"
  revision "master"
  provider Chef::Provider::Deploy::Revision
  user     "pi"
  group    "pi"
  
  # Clear this default railsy configuration, manage it in hooks
  symlink_before_migrate({})
  symlinks({})
  create_dirs_before_symlink []
  purge_before_symlink []
  
  # Trigger the build after the deploy completes
  notifies :execute, "execute[/var/lib/wiringPi/build"
end
  