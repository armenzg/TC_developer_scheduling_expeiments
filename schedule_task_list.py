import ast
import json
import logging
import os
import re
import requests
import time

import taskcluster as taskcluster_client
from mozci import TaskClusterManager
from mozci.utils.log_util import setup_logging

setup_logging(logging.INFO)
credentials = None

try:
    with open('credentials.json', 'r') as file:
        credentials = ast.literal_eval(file.read())
    tc = TaskClusterManager(credentials=credentials)
except IOError:
    tc = TaskClusterManager(web_auth=True)

#resp = requests.get("https://public-artifacts.taskcluster.net/fSQu-SgVTNCroCAgrALLZQ/0/public/full-task-graph.json")
with open("full-task-graph.json", 'r') as json_file:
	full_tasks = json.load(json_file)

# List of task labels I want executed
task_labels = ["TaskLabel==OX3mF4p8RHuMpvHLvd79zg", "TaskLabel==A-5tsSN4QBODXI95Lkzm7w"]

# Needed for Depth First Search
tasks_discovered = []

# Will store dependencies left and taskId
task_data = {}

# Stores the order in which tasks need to be scheduled
# This queue is built using Depth First Search
task_queue = []

while len(task_labels) > 0:
	task_label = task_labels[0]
	if task_label not in tasks_discovered:
		tasks_discovered.append(task_label)
	if task_label not in task_data:
		task_data[task_label] = {
			"dependencies": full_tasks[task_label]["dependencies"].values(),
			"taskId": ""
		}
	# List of remaining dependencies
	dependencies = task_data[task_label]["dependencies"]
	if len(dependencies) == 0:
		# We have satisfied all dependencies, let's execute this task!
		task_label = task_labels.pop(0)
		task_queue.append(task_label)
	else:
		# Let's do the next dependency
		dependency = task_data[task_label]["dependencies"].pop(0)
		# Inserting in the beginning for a depth first search
		# Taking care not to insert tasks already in discovered list
		if dependency not in tasks_discovered:
			task_labels.insert(0, dependency)

for task_label in task_queue:
	task = full_tasks[task_label]['task']

	# Satisfying the <..> fields
	task_json = json.dumps(task)
	references = re.findall(r'{\s*?\r*?\n*?\s*?"task-reference"\s*?:.*?\n*?.*?}', task_json)
	for ref in references:
		ref_string = re.findall(r'<.+?>', ref)[0]
		ref_key = ref_string[1:-1]
		ref_label = full_tasks[task_label]["dependencies"][ref_key]
		new_ref = ref.replace(ref_string, task_data[ref_label]["taskId"])
		ref_dict = json.loads(new_ref)
		task_json = task_json.replace(ref, '"'+ref_dict["task-reference"]+'"')
	task = json.loads(task_json)

	dependencies = full_tasks[task_label]["dependencies"].values()
	task["dependencies"] = []
	for dependency in dependencies:
		task["dependencies"].append(task_data[dependency]["taskId"])
	taskId = tc.schedule_task(task=task)["status"]["taskId"]
	task_data[task_label]["taskId"] = taskId
