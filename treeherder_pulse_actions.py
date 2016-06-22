''' This script adds a hello world job to a local Treeherder instance. '''
import os

# Third party modules
from temp_lib.treeherder_submitter import (
    TreeherderSubmitter,
    TreeherderJobFactory
)

# We're going to schedule to a local instance of Treeherder
# http://local.treeherder.mozilla.org/#/jobs?repo=try&revision=49401a18515d39c96cb0bd56e673dd7ca1acf02a
CLIENT = os.environ['TREEHERDER_CLIENT_ID']
SECRET = os.environ['TREEHERDER_SECRET']
REPOSITORY = 'try'
REVISION = '66537e88c60f84f69cd9f8b779c82cd5ddeee8de'

th = TreeherderSubmitter(
    treeherder_url='http://local.treeherder.mozilla.org',
    treeherder_client_id=CLIENT,
    treeherder_secret=SECRET,
)

job_template = {
    'desc': 'This job represents a scheduling request by a developer processed by pulse_actions',
    'job_name': 'pulse_actions',
    'job_symbol': 'Scheduling',
    'option_collection': 'opt', # Even if 'opt' does not apply to us
}

job_factory = TreeherderJobFactory(submitter=th)
job = job_factory.create_job(
    repository=REPOSITORY,
    revision=REVISION,
    add_platform_info=False,
    **job_template
)

job_factory.submit_running(job)
job_factory.submit_completed(
    job,
    result='success',
    artifacts=[
        {
            'name': 'hey',
            'type': 'text',
            'blob': '{"a": "blob"}'
        },
    ],
)
