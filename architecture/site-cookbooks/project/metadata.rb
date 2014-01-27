name              "homepi"
maintainer        "Andrew Coulton"
maintainer_email  "andrew@ingenerator.com"
license           "BSD"
description       "Installs and configures the home raspberry pi monitoring"
version           "0.0.1"

depends "ingenerator-php"

%w{ ubuntu debian }.each do |os|
  supports os
end
