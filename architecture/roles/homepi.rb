# The homepi role

name "homepi"
description "Raspberry Pi running home monitoring"

# Additional systems are loaded in the dev-server recipe, which is dynamically
# included by the app-server role if required.
run_list(
  "recipe[project::homepi]"
)

override_attributes({
  'php' => {
    'directives' => {
      'apc.stat' => 1,
    },
  },
  'bashrc' => {
    'rolename'  => 'homepi',
    'env'       => 'LIVE',
    'env_color' => '$Red'
  }
})
