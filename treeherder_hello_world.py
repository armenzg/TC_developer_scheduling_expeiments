''' This script adds a hello world job to a local Treeherder instance. '''
import os
import socket
import uuid

from taskcluster.utils import slugId, fromNow

from thclient import (
    TreeherderClient,
    TreeherderJobCollection
)

# We're going to schedule to a local instance of Treeherder
# http://local.treeherder.mozilla.org/#/jobs?repo=try&revision=49401a18515d39c96cb0bd56e673dd7ca1acf02a
client = os.environ['TREEHERDER_CLIENT_ID']
secret = os.environ['TREEHERDER_SECRET']


dataset = [
    {
        'project': 'try',
        'revision': '49401a18515d39c96cb0bd56e673dd7ca1acf02a',
        'job': {
            'job_guid': str(uuid.uuid4()),
            'who': 'local_script',
            'desc': 'We want to show a hello world job',
            'name': 'Hello World!',
            'product_name': 'no product',
            'job_symbol': 'HW',
            'submit_timestamp': fromNow('0m'),
            'start_timestamp': fromNow('1m'), #XXX
            'end_timestamp': fromNow('2m'),
            'state': 'completed',
            'result': 'success',
            'tier': 2,
            'artifacts': [{
                'type': 'json',
                'name': '',
                'blob': '{hello world}'
            }],
            # List of job guids that were coalesced to this job
            'coalesced': []
        },
    },
]

tjc = TreeherderJobCollection()

for data in dataset:
    tj = tjc.get_job()

    tj.add_revision(data['revision'])
    tj.add_project(data['project'])
    job = data['job']
    tj.add_coalesced_guid(job['coalesced'])
    tj.add_job_guid(job['job_guid'])
    tj.add_job_name(job['name'])
    tj.add_job_symbol(job['job_symbol'])
    tj.add_description(job['desc'])
    tj.add_product_name(job['product_name'])
    tj.add_state(job['state'])
    tj.add_result(job['result'])
    tj.add_who(job['who'])
    tj.add_tier(job['tier'])
    tj.add_submit_timestamp(job['submit_timestamp'])
    tj.add_start_timestamp(job['start_timestamp'])
    tj.add_end_timestamp(job['end_timestamp'])

    # job['artifact'] is a list of artifacts
    for artifact_data in job['artifacts']:
        tj.add_artifact(
            artifact_data['name'],
            artifact_data['type'],
            artifact_data['blob']
        )

    # We add the Treeherder job to the Treeherder job collection
    tjc.add(tj)

client = TreeherderClient(
    protocol='https',
    host='local.treeherder.mozilla.org',
    client_id=client, secret=secret
)
client.post_collection('try', tjc)
