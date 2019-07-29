"""
Source code for accessing and uploading to AWS S3.
"""

import subprocess


# TODO: check if project/client/archive already exists (case senstive)

def configure_awscli():
    subprocess.run(
        ['aws', 'configure'], 
        creationflags=subprocess.CREATE_NEW_CONSOLE,
        )

def _build_s3uri(bucket, local_dir):
    s3_loc = '/'.join(local_dir.split('/')[1:])
    return f's3://{bucket}/{s3_loc}/'

def run_upload(bucket, local_dir, ignore_folders=None):
    excludes = []
    if ignore_folders:
        for directory in ignore_folders:
            excludes.append('--exclude')
            excludes.append(f'{directory}/*')

    s3uri = _build_s3uri(bucket, local_dir).lower()
    subprocess.run(
        [
            'cmd', '/K', 'aws', 's3', 'cp', 
            local_dir, 
            s3uri,
            "--recursive", '--exclude', "*",
            '--include', "*.zip", '--include', "*.rar", *excludes,
        ], 
        creationflags=subprocess.CREATE_NEW_CONSOLE,
        )
