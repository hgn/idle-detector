Shutdown (or execute command) if for a given time no traffic was recognized.
Edit ```idle-detector.py``` to configure the observed protocols and ports.
Currently the script is limited to UDP/TCP, but whole iptables protocol set is
possible.

## Implemenation ##

Use iptables IDLETIMER target and inotify to trigger for event. Probably the
most efficient way to do this with Linux.

## Installation ##

make install

## Configuration ##

See first line in idle-detector.py

## Systemd Integration ##

Make install already installed the required service files for systemd. Simple
enable and start the service and it should work:

systemctl enable /etc/systemd/system/idle-detector.service
systemctl start idle-detector.service
systemctl status idle-detector.service
