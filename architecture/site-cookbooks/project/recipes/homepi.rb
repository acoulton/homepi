# Homepi recipe
# To be refactored!

# Activate IO kernel modules - note this will require a reboot after install
cookbook_file "/etc/modules" do
  source "etc/modules"
  owner  "root"
  group  "root"
  mode   0644
end

# Directories
directory "/home/pi/homepi/tmp/last-room-temps/" do
  owner "pi"
  group "pi"
  recursive true
end

# Install wiringPi
include_recipe "project::wiringpi"

# Install python stuff
include_recipe "project::python_modules"
include_recipe "project::crons"
