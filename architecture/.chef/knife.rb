# Default organisation-wide knife config file. Do not
# place sensitive credentials in this file, use
# environment variables to load from the user's local
# configuration.

# Setup the default cookbook copyright 
cookbook_copyright "Andrew Coulton"
cookbook_email     "andrew@ingenerator.com"
cookbook_license   "apachev2"

# Setup paths for cookbooks, roles and data bags
# Note that these also need to be changed in the 
# vagrant config and chef-solo config if the 
# repository layout changes
chef_root_dir = File.join(File.dirname(__FILE__),'..')

# Set the chef file paths
cookbook_path    File.join(chef_root_dir, "cookbooks")
role_path        File.join(chef_root_dir, "roles")
data_bag_path    File.join(chef_root_dir, "data_bags")
