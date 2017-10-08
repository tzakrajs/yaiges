##Cloud-Fortress Miniframework
* Written by Thomas Zakrajsek

### What?
* This is a python3 microframework based on Tornado
* Uses the python3 asyncio library for asynchronous processing
* Listens on IPv4 and IPv6 simultaneously
* Provides listeners for HTTP, HTTPS, WS, WSS simultaneously
* Simple MVC-based structure for expanding capability
* Can also be used with wsgi, if you point the WSGIScriptAlias at the `run_server.py` file

### Why?
* Because I was bored, of course!

### Install
* Use `pip install -r requirements.txt` to install Python dependencies
* Edit the `config.yml` to your hearts content
* If using djb daemontools supervise, edit the `run` file to include the path that this project has been installed to, otherwise the imports will break

### Support?
* Open an issue on GitHub if you have any problems: https://github.com/tzakrajs/cloud-fortress-www
