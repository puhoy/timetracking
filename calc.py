import humanize
import datetime
import sys
import os
import json

save_dir = 'saves'

if len(sys.argv) < 2:
	print("usage: python3 " + __file__ + "projectname")
	exit(0)


project_name = sys.argv[1]

save_file = os.path.join(save_dir, project_name + '_times.json')
all_times =  {}

if os.path.isfile(save_file):
	print("opening " + save_file)
	f = open(save_file, 'r')
	try:
		all_times = json.loads(f.read())
		print(all_times)
	except ValueError:
		print('value error while reading json file')
		exit(0)
		pass
	f.close()

if not all_times:
	exit(0)

for key in all_times:
	print(datetime.datetime.fromtimestamp(float(key)))