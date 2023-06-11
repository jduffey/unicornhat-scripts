# unicornhat-scripts
Scripts designed for the Pimoroni Unicorn HAT HD Raspberry Pi display module.

# Instructions

## Set up virtual environment

- `python3 -m venv --system-site-packages venv`
   - This command gives our virtual environment access to system-install packages which are needed by Numpy.
- `source venv/bin/activiate`

## Install dependencies
- `pip3 install -r requirements.txt`

## Run script
- `python3 eth_base_fee.py`


# Instructions for running automatically when Raspberry Pi starts

## Create the .service file
- Create `/etc/systemd/system/unicornhathd.service` with the following contents.
- _Make sure to replace the **script paths** and **user** with the correct values for your system!_
```
[Unit]
Description=Unicorn HAT HD Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/your/python/script.py
WorkingDirectory=/path/to/your/python/
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```

## Configure the service to start on boot
- `systemctl enable unicornhathd.service`
   - This command adds the service to the directory indicated in the .service file; in this case we install the service at `/etc/systemd/system/multi-user.target.wants`

## Notes

These instructions were tested on the `Raspbian GNU/Linux 11 (bullseye)` operating system.

To view to status of the service:
- `systemctl status unicornhathd.service`

To view logs of the service (for troubleshooting/debugging):
- `journalctl -u unicornhathd.service`