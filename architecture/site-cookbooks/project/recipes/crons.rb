# Manage crons
cron "water-temperature" do
  action  :create
  minute  "*/5"
  user    "pi"
  home    "/home/pi/homepi"
  command "/home/pi/homepi/scripts/water-temp.sh"
end

cron "room-temperature" do
  action  :create
  minute  "*/5"
  user    "pi"
  home    "/home/pi/homepi"
  command "/home/pi/homepi/scripts/room-temp.sh"
end
