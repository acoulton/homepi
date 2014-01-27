#!/bin/bash

# Ensures that the correct Chef version is properly installed, using the omnibus installer from
# Opscode. This script runs as part of instance provisioning whether on a Vagrant or remote host
# prior to running the chef-solo provisioning code.
#
# Copyright: 2013 inGenerator Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Set this to the Chef version required
require_version="11.8.0"

# --------------------------------------------------------------------------------------------------
# Do not edit beyond here.
# --------------------------------------------------------------------------------------------------

# Don't accept unset variables
set -o nounset
# Exit on failed commands
set -o errexit
# Trap error exit and report failure
function error_handler()
{
    echo "********************************************************"
    echo "* PROVISIONING FAILED - SEE COMMAND OUTPUTS ABOVE      *"
    echo "********************************************************"
}
trap 'error_handler' ERR

# Check if chef is currently installed
have_chef=`which chef-solo || true`

if [ -n "$have_chef" ]; then
  # Chef is installed, check the version
  ver_str=`chef-solo -v`
  regex='^Chef: [0-9]+\.[0-9]+\.[0-9]+$'
  if [[ ! ("$ver_str" =~  $regex) ]]; then
    echo "ERROR: Invalid version string '$ver_str' returned from chef-solo"
    exit 999
  fi

  # Extract the version number - this is safe because we have already tested the format
  set $ver_str
  installed_ver=$2
  echo "Chef version '$installed_ver' is currently installed"

  # If the version number matches requirement, just return with success
  if [ "$installed_ver" = "$require_version" ]; then
    echo "Required version '$require_version' is already installed - nothing to do"
    exit 0
  fi
else
  echo "Chef is not currently installed"
fi

# If execution reaches this point then either Chef is not installed, or it's the wrong version
echo "Installing Curl"
sudo apt-get install -y curl

echo "Installing Chef version '$require_version'"
sudo curl -L https://www.opscode.com/chef/install.sh > /tmp/chef-install.sh
sudo chmod +x /tmp/chef-install.sh
sudo /tmp/chef-install.sh -v $require_version
