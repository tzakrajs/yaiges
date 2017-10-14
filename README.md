## Yaiges
* Written by Thomas Zakrajsek
* Pronounced: *yeah i guess*

### What?
* Enterprise-minded Monitoring and Alerting solution
* Tornado with Python3 AsyncIO loop
* Intended to run as a long-running daemon
* Default persistence module is for MySQL/MariaDB

### Why?
* Because everyone complains about Nagios and then continues to use it

### Install
* Use `pip install -r requirements.txt` to install Python dependencies
* Edit the `config.yml` to your hearts content
* If using djb daemontools supervise, edit the `run` file to include the path that this project has been installed to, otherwise the imports will break

### Support?
* Open an issue on GitHub if you have any problems: https://github.com/tzakrajs/yaiges
