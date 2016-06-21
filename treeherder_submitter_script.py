''' This script adds a hello world job to a local Treeherder instance. '''
import os

# Third party modules
from thsubmitter import (
    TreeherderSubmitter,
    TreeherderJobFactory
)

# We're going to schedule to a local instance of Treeherder
th = TreeherderSubmitter(
    treeherder_url='http://local.treeherder.mozilla.org',
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

job_factory = TreeherderJobFactory(submitter=th)
job = job_factory.create_job(
    repository='try',
    revision='66537e88c60f84f69cd9f8b779c82cd5ddeee8de',
    add_platform_info=True,
    **job_template
)

job_factory.submit_running(job)
job_factory.submit_completed(
    job=job,
    result='success', # XXX: This should be a constant
    job_info=[
        {
            "url": "https://www.mozilla.org",
            "value": "website",
            "content_type": "link",
            "title": "Mozilla home page"
        }
    ],
    artifacts=[],
)
