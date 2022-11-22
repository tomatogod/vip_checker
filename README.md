# vip_checker
Simple check if redis is master of a cluster and that secondary ip (VIP) is present, if not add it. 


Goals:

- Should work without installing any non default python modules
- Should check if Redis Role = Master or not
- Should check if defined secondary IP address exists on host
- Should stay local and not require any firewall ports to be open
- Relies on Redis cluster to elect / manage master / replica statuses.
- Should poll to check regularly

PreRequisites:

- Python (tested on version 3.9.2)
- Linux Machine
- User account with sufficient privedges to install systemd service and add a secondary ip address
- Redis running on local machine with authentication enabled
- Within the script we run a 'sudo' command, in order to allow the running user to complete this command you'll need to allow that account within the sudoers file without a password.
	sudo nano /etc/sudoers
	edit "# User privilege specification" section and add the following line:
	redis	ALL=NOPASSWD: ALL

Suggested Installation Instructions

- copy vip_checker.py into /etc/redis/
- edit vip_check.config with editor and configure the 'configuration items'
-   vip = is the secondary IP address that will act as the Virtual IP Address (VIP)
-   mask = subnet mask of the vip
-   device = device name where the secondary ip address should be hosted on
-   redis_auth_password = requirepass setting within redis.conf
-   time_to_sleep = amount of time in seconds between poll of checker.
- copy vip_checker.service to /etc/systemd/system/
- edit if required - current setup to utilize the 'redis' user which may or may not already be present in your setup.
- enable vip_checker service and start
