import ast
import json
import logging
import os

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


with open(os.path.join('artifacts', 'linux64_test_task.json')) as file:
    task = json.load(file)

# https://groups.google.com/d/msg/mozilla.tools.taskcluster/nkzBlX7BgrU/-IrWXPXCAQAJ
# This prevents us from scheduling a task which would show up on Treeherder
task['routes'] = []
tc.schedule_task(task=task)
