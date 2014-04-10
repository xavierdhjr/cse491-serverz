first, we need to transfer our files (WinSCP on Windows)
	Open WinSCP and select NEw Site
	Change File Protocol to 'SCP'
	Fill in the hostname with the value under the Amazon AWS console -> Instances under DNS NAme
		(for the one i setup, it's ec2-54-186-240-224.us-west-2.compute.amazonaws.com)
	Set username to 'ubuntu'
	Now we need to setup our private key that we got when we setup our AWS instance
		Open puttyGen
		Load
		Select the *.* all files dropdown option
		Choose the .pem private key downloaded earlier
		Save the private key 
		Now go back to WinSCP
	Click 'Advanced' and go to SSH -> Authentication
	Find the private key file you just saved under Authentication Parameters
	Hit OK and Save
	Login to WinSCP and transfer files

SSH into your AWS instance (similar setup as above, except in puttySSH)
	
install pip (sudo apt-get install python-pip)
install virtualenv (sudo apt-get install python-virtualenv)
Make sure everything is up to date (sudo apt-get update)
Install python development headers (sudo apt-get install python-dev)

enter virtualenv (source bin/activate)
Install quixote (pip install quixote)
Install jinja2 (pip install jinja2)

Go to AWS console -> Network & Security / Security Groups
Add new inbound rule
HTTP, TCP, Port 80, Source 0.0.0.0/0
This will allow for users to enter on port 80

check port forwarding (cat /proc/sys/net/ipv4/ip_forward)
	if 0, its disabled.
	
If port forwarding is disabled
	Open config (sudo vim /etc/sysctl.conf)
	Uncomment net.ipv4.ip_forward
	Save
	Enable Changes (sudo sysctl -p /etc/sysctl.conf)
	Check if changes were successful (cat /proc/sys/net/ipv4/ip_forward)
	Should return 1

To run on port XXXX, setup forwarding
sudo iptables -A PREROUTING -t nat -i eth0 -p tcp --dport 80 -j REDIRECT --to-port XXXX

Open firewall
sudo iptables -A INPUT -p tcp -m tcp --sport 80 -j ACCEPT
sudo iptables -A OUTPUT -p tcp -m tcp --dport 80 -j ACCEPT

Run server.py on port XXXX

WELCOME TO THE CLOUD