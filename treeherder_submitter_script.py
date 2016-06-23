''' This script adds a hello world job to a local Treeherder instance. '''
import os
import logging

# Third party modules
from thsubmitter import (
    TreeherderSubmitter,
    TreeherderJobFactory
)

LOG = logging.getLogger()
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

# We're going to schedule to a local instance of Treeherder
th = TreeherderSubmitter(
    host=os.environ['TREEHERDER_HOST'],
    protocol='http' if os.environ['TREEHERDER_HOST'].startswith('local') else 'https',
    treeherder_client_id=os.environ['TREEHERDER_CLIENT_ID'],
    treeherder_secret=os.environ['TREEHERDER_SECRET'],
)

job_template = {
    'desc': 'A hello world description!',
    'job_name': 'hello_world',
    'job_symbol': 'HelloWorld',
    # Even if 'opt' does not apply to us
    'option_collection': 'opt',
    # Used if add_platform_info is set to True
    'platform_info': ('linux', 'other', 'x86_64'),
}

DRY_RUN = False

job_factory = TreeherderJobFactory(submitter=th)
job = job_factory.create_job(
    repository='try',
    revision='303b2c6cbc20d3847b5fdfcffb45351bbe59ed1b',
    add_platform_info=True,
    **job_template
)

job_factory.submit_running(job, dry_run=DRY_RUN)

job_factory.submit_completed(
    job=job,
    result='success', # XXX: This should be a constant
    job_info_details_panel=[
        {
            "url": "http://people.mozilla.org/~armenzg/permanent/all_builders.txt",
            "value": "all_builders.txt",
            "content_type": "link",
            "title": "All Buildbot builders"
        },
    ],
    log_references=[
        {
            "url": "http://people.mozilla.org/~armenzg/permanent/all_builders.txt",
            "name": "unittest",
            "parse_status": "parsed"
        }
    ],
    artifacts=[],
    dry_run=DRY_RUN,
)
