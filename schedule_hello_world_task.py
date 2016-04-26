import json
import logging
import os
import webbrowser

from mozci.taskcluster import TaskClusterManager, get_task_inspector_url
from mozci.utils.log_util import setup_logging

setup_logging(logging.INFO)

tc = TaskClusterManager(web_auth=True)

with open(os.path.join('artifacts', 'hello_world_task.json')) as file:
    task = json.load(file)

task = tc.schedule_task(task=task)
webbrowser.open_new_tab(url=get_task_inspector_url(task['status']['taskId']))
