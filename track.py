from Xlib.display import Display
import time as t
import datetime

import os
import sys
import json

import git

if len(sys.argv) < 2:
	print("usage: python3 " + __file__ + "projectname")
	exit(0)


def save_session():
	print('ftimes: ' + str(focus_times))

	save_file = os.path.join(save_dir, project_name + '_times.json')
	
	all_times =  {}
	if os.path.isfile(save_file):
		f = open(save_file, 'r')
		try:
			all_times = json.loads(f.read())
		except ValueError:
			pass
		f.close()

	all_times[start] = {}

	focus_times['end_time'] = str(t.time())
	all_times[start] = focus_times

	print('alltimes: ' + str(all_times))
	
	f = open(save_file, 'w+')
	json.dump(all_times, f, indent=4)
	f.close()

	if os.path.exists(os.path.join(save_dir, '.git')):
		repo = git.Repo(os.path.join(os.getcwd(), save_dir))	
		repo.git.add([repo.untracked_files])
		repo.index.commit(project_name)
		repo.remotes.origin.push(repo.head)


#import atexit
#atexit.register(save_session)

display = Display()

interval = 1

focus_times = {}

project_name = sys.argv[1]

save_dir = 'saves'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)


start = str(t.time())
focus_times = {}

running=True

while(running):
	
	window = display.get_input_focus().focus
	#print(window)
	wmname = window.get_wm_name()
	wmclass = window.get_wm_class()

	if wmclass is None and wmname is None:#
		window = window.query_tree().parent
		wmname = window.get_wm_name()

	if wmname:
		if not focus_times.get(wmname, None):
			focus_times[wmname] = {}

		time = focus_times[wmname].get('time', None)
		if not time:
			focus_times[wmname]['time'] = interval
		else:
			focus_times[wmname]['time'] += interval
	print(focus_times)


	try:
		t.sleep(interval)
	except KeyboardInterrupt:
		print('got interrupt')
		running=False

save_session()

