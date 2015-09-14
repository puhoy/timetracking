import humanize
import datetime
import sys
import os
import json
import time


def percentage_activity(focus_activity):
	time_percentage = {}
	sum_time = 0

	for wmname in focus_activity.keys():
		sum_time += focus_activity[wmname].get('time')

	for wmname in focus_activity.keys():
		time_percentage[wmname] = float(focus_activity[wmname].get('time')) * 100 / sum_time

	return time_percentage

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
		
	except ValueError:
		print('value error while reading json file')
		exit(0)
		pass
	f.close()

if not all_times:
	exit(0)
print("your stats for " + sys.argv[1])
print()
whole_time = 0

for key in all_times.keys():
	#print(all_times[key])
	start_time = datetime.datetime.fromtimestamp(float(key))
	start_time_readable = start_time.strftime("%Y-%m-%d %H:%M")
	end_time = datetime.datetime.fromtimestamp(float(all_times[key].get('end_time', None)))
	end_time_readable = end_time.strftime("%Y-%m-%d %H:%M")

	diff = float(all_times[key].get('end_time', None)) - float(key)
	diff_datetime = datetime.timedelta(seconds=diff)
	whole_time += (float(all_times[key].get('end_time', None)) - float(key))
	print('Session: (' + humanize.naturalday(start_time) + ') ' + ' duration: ' +  str(diff_datetime) + 's')
	
	print( str(start_time_readable) + ' - ' + end_time_readable)

	if all_times[key].get('description', None):
		print(' description: ' + all_times[key].get('description', None))

	perc_act = percentage_activity(all_times[key].get('focus_times'))

	for wmname in perc_act.keys():
		print('  ' + str(round(perc_act[wmname], 2)) + "% - " + wmname[:25])
	
	
	print()
	
print('whole time spent on this project: ' + str(datetime.timedelta(seconds=whole_time)))



