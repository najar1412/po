"""
Source code for accessing and uploading to AWS S3.
"""

# TODO: Check for awscli install
# TODO: check awscli credentuals

import subprocess

def _build_s3uri(bucket, local_dir):
    s3_loc = '/'.join(local_dir.split('/')[1:])
    return f's3://{bucket}/{s3_loc}/'


def run_upload(bucket, local_dir):
    s3uri = _build_s3uri(bucket, local_dir)
    subprocess.run([
        'cmd', '/k', 'aws', 's3', 'cp', 
        local_dir, 
        s3uri, 
        '--recursive', '--exclude', '*', 
        '--include', '*.zip', '--include', '*.rar'
        ], creationflags=subprocess.CREATE_NEW_CONSOLE)
