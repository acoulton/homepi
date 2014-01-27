# Configuration and setup for chef-solo

file_cache_path "/var/chef-solo/cache"

if ! File.exists? "/var/chef-solo/cache"
  require 'fileutils'
  FileUtils.mkdir_p "/var/chef-solo/cache", :mode => 0755
end



# Setup paths for cookbooks, roles and data bags
# Note that these also need to be changed in the 
# vagrant config and knife config if the 
# repository layout changes
chef_root_dir = File.expand_path('..',File.dirname(__FILE__))

# Set the chef file paths
cookbook_path    [File.join(chef_root_dir, "site-cookbooks"), File.join(chef_root_dir, "vendor-cookbooks")]
role_path        File.join(chef_root_dir, "roles")
data_bag_path    File.join(chef_root_dir, "data_bags")
