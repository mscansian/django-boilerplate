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
current_user = getpass.getuser()

if not os.path.isdir(gunicorn_dir):
    print ("Creating gunicorn configuration dir")
    os.mkdir(gunicorn_dir)

print ("Generating start_gunicorn.sh")
context = {
    "GENERATOR_PROJECTNAME": project_name,
    "GENERATOR_DJANGODIR": os.path.join(cwd, "src"),
    "GENERATOR_SOCKFILE": os.path.join(gunicorn_dir, "gunicorn.sock"),
    "GENERATOR_USER": current_user,
    "GENERATOR_GROUP": current_user,
    "GENERATOR_WORKERS": "3",
}
with open("scripts/templates/start_gunicorn") as f:
    template = string.Template(f.read())
data = template.substitute(context)
with open(os.path.join(gunicorn_dir, "start_gunicorn.sh"), "w") as f:
    f.write(data)
os.chmod(os.path.join(gunicorn_dir, "start_gunicorn.sh"), 0755)

print ("Generating supervisor.conf")
context = {
    "PROJECTNAME": project_name,
    "COMMAND": os.path.join(gunicorn_dir, "start_gunicorn.sh"),
    "USER": current_user,
    "LOGFILE": os.path.join(gunicorn_dir, "gunicorn.log"),
}
with open("scripts/templates/supervisor") as f:
    template = string.Template(f.read())
data = template.substitute(context)
with open(os.path.join(gunicorn_dir, "supervisor.conf"), "w") as f:
    f.write(data)

create_link = raw_input("Do you want to create gunicorn link to supervisor? (yes/NO)? ")
if create_link.lower() == "yes":
    print ("Creating supervisor link...")
    print ("sudo ln -s {} /etc/supervisor/conf.d/{}.conf".format(
        os.path.join(gunicorn_dir, "supervisor.conf"), project_name))
    os.system("sudo ln -s {} /etc/supervisor/conf.d/{}.conf".format(
        os.path.join(gunicorn_dir, "supervisor.conf"), project_name))
    print ("Loading supervisor...")
    print ("sudo supervisorctl reread && sudo supervisorctl update")
    os.system("sudo supervisorctl reread && sudo supervisorctl update")
    print ("sudo supervisorctl status {}".format(project_name))
    os.system("sudo supervisorctl status {}".format(project_name))
    print ("All set! Have a nice day :)")
else:
    print ("")
    print ("All files were created under 'gunicorn' folder, but you still need to configure supervisor:")
    print ("sudo ln -s {} /etc/supervisor/conf.d/{}.conf".format(
        os.path.join(gunicorn_dir, "supervisor.conf"), project_name))
    print ("sudo supervisorctl reread && sudo supervisorctl update")
    print ("sudo supervisorctl status {}".format(project_name))

