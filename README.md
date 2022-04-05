# vip_checker
Simple check if redis is master of a cluster and that secondary ip (VIP) is present, if not add it. 


Goals:

- Should work without installing any non default python modules
- Should check if Redis Role = Master or not
- Should check if defined secondary IP address exists on host
- Should stay local and not require any firewall ports to be open
- Relies on Redis cluster to elect / manage master / replica statuses.
- Should poll to check regularly
