#!/bin/bash

# Ensures that the instance has the correct Ruby version and the berkshelf gem and then installs
# the berkshelf-managed cookbooks
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

# Check if we need to install berkshelf first
have_berks=`which berks || true`
if [ -z "$have_berks" ]; then
  echo "Berkshelf not found, installing it with dependencies"

  echo "Updating apt cache"
  sudo apt-get update

  echo "Installing build essentials"
  sudo apt-get install -y -q build-essential

  echo "Installing Ruby 1.9.3"
  sudo apt-get install -y -q ruby1.9.3

  echo "Installing nokogiri dependencies"
  sudo apt-get install -y -q libxslt-dev libxml2-dev

  echo "Installing berkshelf"
  sudo gem install berkshelf

  echo "Installing git"
  sudo apt-get install -y git
fi
