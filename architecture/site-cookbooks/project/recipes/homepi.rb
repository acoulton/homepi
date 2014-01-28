# Homepi recipe
# To be refactored!

# Activate IO kernel modules - note this will require a reboot after install
cookbook_file "/etc/modules" do
  source "etc/modules"
  owner  "root"
  user   "root"
  mode   0644
end

# Install wiringPi
include_recipe "project::wiringpi"