# Docmentation

## Installation

### Pre Install
Ubuntu/Debian:
`sudo apt-get install python3 python3-pip3`

### Clone Repository
with SSH:
`git clone git@github.com:tosterkamp/random-redirect.git`
with HTTPS:
`git clone https://github.com/tosterkamp/random-redirect.git`

enter directory:
`cd random-redirect`

### Install
create virtual environment:
`python3 -m venv ./venv`

source venv file:
`source venv/bin/activate`

install python requirements:
`pip install -r requirements.txt`

create systemd service:
`cp random-redirect.service /etc/systemd/system/random-redirect.service`
`sudo systemctl daemon-reload`

start systemd service:
`sudo systemctl start random-redirect.service`

check service output:
`sudo journalctl -f -u random-redirect.service`
