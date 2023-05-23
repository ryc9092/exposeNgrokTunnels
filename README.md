# exposeNgrokTunnels
Get ngrok tunnels info of device by email when tunnels has changed

### Description
This program will send ngrok tunnels info by email when tunnels has changed (maybe device reboot)

### Pre-requirements
- Ngrok
Use `~/.config/ngrok/ngrok.yml` to create multiple tunnels by command: `ngrok start --all --config '~/.config/ngrok/ngrok.yml'`, and make it auto start (by service/crontab...).

### Usage
1. Get google app password for send email
2. Edit sender, receiver, password in emailConfiguration.yaml
3. Put the job to crontab: `*/5 * * * * cd /path/to/ExposeNgrokTunnels && python3 /path/to/ExposeNgrokTunnels/main.py`