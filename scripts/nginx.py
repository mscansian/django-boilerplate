#!/usr/bin/python
from __future__ import print_function
import getpass
import os
import stat
import string
import sys


cwd = os.getcwd()
project_name = sys.argv[1]
gunicorn_dir = os.path.join(cwd, "gunicorn")
nginx_dir = os.path.join(cwd, "nginx")

if not os.path.isdir(nginx_dir):
    print ("Creating nginx configuration dir")
    os.mkdir(nginx_dir)

server_name = raw_input("Please enter 'server_name' (eg. example.com) ")

print ("Generating nginx.conf")
context = {
    "GENERATOR_PROJECTNAME": project_name,
    "GENERATOR_DJANGODIR": os.path.join(cwd, "src"),
    "GENERATOR_SOCKFILE": os.path.join(gunicorn_dir, "gunicorn.sock"),
    "GENERATOR_SERVERNAME": server_name,
    "GENERATOR_NGINXDIR": nginx_dir
}
with open("scripts/templates/nginx") as f:
    template = string.Template(f.read())
data = template.substitute(context)
with open(os.path.join(nginx_dir, "nginx.conf"), "w") as f:
    f.write(data)

create_link = raw_input("Do you want to install this website in nginx? (yes/NO)? ")
if create_link.lower() == "yes":
    print ("Creating sites-available link...")
    print ("sudo ln -s {} /etc/nginx/sites-available/{}".format(
        os.path.join(nginx_dir, "nginx.conf"), project_name))
    os.system("sudo ln -s {} /etc/nginx/sites-available/{}".format(
        os.path.join(nginx_dir, "nginx.conf"), project_name))
    print ("Creating sites-enabled link...")
    print ("sudo ln -s /etc/nginx/sites-available/{} /etc/nginx/sites-enabled/{}".format(
        project_name, project_name))
    os.system("sudo ln -s /etc/nginx/sites-available/{} /etc/nginx/sites-enabled/{}".format(
        project_name, project_name))
    print ("Restarting nginx...")
    print("sudo service nginx restart")
    os.system("sudo service nginx restart")
    print ("All set! Have a nice day :)")
else:
    print ("")
    print ("All files were created under 'nginx' folder, but you still need to configure it:")
    print ("sudo ln -s {} /etc/nginx/sites-available/{}".format(
        os.path.join(nginx_dir, "nginx.conf"), project_name))
    print ("sudo ln -s /etc/nginx/sites-available/{} /etc/nginx/sites-enabled/{}".format(
        project_name, project_name))
    print("sudo service nginx restart")
