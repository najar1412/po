import pathlib
import os


def build_job(root, client, project, job):
    # TODO: figure out error proof way of using project code
    # TODO: Imple folder struct in code
    base = pathlib.Path(root, client, project, job)

    return base
    
    