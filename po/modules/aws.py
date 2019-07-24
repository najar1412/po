"""
Source code for accessing and uploading to AWS S3.
"""

import os
import subprocess
from distutils.spawn import find_executable

# TODO: check if project/client/archive already exists (case senstive)

def is_awscli_installed():
    if find_executable('aws'):
        return True
    else:
        return False


def does_aws_config_exist():
    home = os.path.expanduser('~')

    if os.path.exists(f'{home}\\.aws'):
        if not os.path.isfile(f'{home}\\.aws\\credentials'):
            configure_awscli()
        else:
            True
    else:
        os.mkdir(f'{home}\\.aws')
        configure_awscli()

    return True


def configure_awscli():
    subprocess.run(
        ['aws', 'configure'], 
        creationflags=subprocess.CREATE_NEW_CONSOLE,
        )


def _build_s3uri(bucket, local_dir):
    s3_loc = '/'.join(local_dir.split('/')[1:])
    return f's3://{bucket}/{s3_loc}/'


def run_upload(bucket, local_dir):
    s3uri = _build_s3uri(bucket, local_dir).lower()
    subprocess.run(
        [
            'cmd', '/k', 'aws', 's3', 'cp', 
            local_dir, 
            s3uri, 
            '--recursive', '--exclude', '*', 
            '--include', '*.zip', '--include', '*.rar'
        ], 
        creationflags=subprocess.CREATE_NEW_CONSOLE,
        )
