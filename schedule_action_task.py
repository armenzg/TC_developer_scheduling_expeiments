import ast
import json
import logging
import os
import requests
import sys
import yaml

import taskcluster as taskcluster_client
from mozci import TaskClusterManager
from mozci.utils.log_util import setup_logging

TC_QUEUE_URL = 'https://queue.taskcluster.net/v1/task/'

setup_logging(logging.INFO)
credentials = None

try:
    with open('credentials.json', 'r') as file:
        credentials = ast.literal_eval(file.read())
    tc = TaskClusterManager(credentials=credentials)
except IOError:
    tc = TaskClusterManager(web_auth=True)

decision_task_id = sys.argv[1]
task_labels = sys.argv[2]
url = TC_QUEUE_URL + decision_task_id + "/artifacts/public/action.yml"
text = requests.get(url).text
text = text.replace("{{decision_task_id}}", decision_task_id)
text = text.replace("{{task_labels}}", task_labels)
task = yaml.load(text)
text = json.dumps(task, indent=4, sort_keys=True)
# https://groups.google.com/d/msg/mozilla.tools.taskcluster/nkzBlX7BgrU/-IrWXPXCAQAJ
# This prevents us from scheduling a task which would show up on Treeherder

tc.schedule_task(task=json.loads(text))
