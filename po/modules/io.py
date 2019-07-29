import pathlib
import os
import json
from distutils.spawn import find_executable


# TODO: scan project dir
# TODO: report directors over the standard windows dir length
# TODO: make project folders
# TODO: display drive projects
# TODO: archive project


def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


def _aws_cred_location():
    home = os.path.expanduser('~')
    return os.path.join(home, '.aws')


def is_awscli_installed():
    if find_executable('aws'):
        return True
    else:
        return False


def check_aws_config():
    """checks for AWS cred files"""
    aws_loc = _aws_cred_location()

    if os.path.exists(aws_loc):
        if os.path.isfile(f'{aws_loc}\\credentials'):
            return True
        else:
            False
    else:
        return False


def read_aws_cred():
    aws_cred_loc = os.path.join(_aws_cred_location(), 'credentials')
    aws_config_loc = os.path.join(_aws_cred_location(), 'config')
    data = {}

    with open(aws_cred_loc, 'r', encoding='utf-8') as aws_cred:
        lines = aws_cred.readlines()
        for line in lines:
            if not line.startswith('['):
                parsed = line.rstrip().split(' = ')
                data[parsed[0]] = parsed[1]

    with open(aws_config_loc, 'r', encoding='utf-8') as aws_config:
        lines = aws_config.readlines()
        for line in lines:
            if not line.startswith('['):
                parsed = line.rstrip().split(' = ')
                data[parsed[0]] = parsed[1]

    return data


def drive_exist(letter):
    bla = pathlib.Path(f"{letter}:").exists()
    return bla


def read_default_config_file(file):
    with open(file) as json_file:
        data = json.loads(json_file.read())

    return data


def write_default_config_file(file, new_data):
    with open(file, 'r+') as json_file:
        json_file.truncate(0)
        json_file.write(json.dumps(new_data))

    return True


def write_aws_config_file(new_data):
    aws_loc = _aws_cred_location()
    aws_cred = f'{aws_loc}\\credentials'
    aws_config = f'{aws_loc}\\config'
    
    with open(aws_cred, 'r+') as json_file:
        json_file.truncate(0)
        json_file.write('[default]\n')
        for k, v in new_data.items():
            if k == 'aws_access_key_id':
                json_file.write(f'{k} = {v}\n')
            if k == 'aws_secret_access_key':
                json_file.write(f'{k} = {v}\n')

    with open(aws_config, 'r+') as json_file:
        json_file.truncate(0)
        json_file.write('[default]\n')
        for k, v in new_data.items():
            if k == 'region':
                json_file.write(f'{k} = {v}\n')
            if k == 'output':
                json_file.write(f'{k} = {v}\n')

    return True


class Manager():
    """tools built around default project structure.
    root: str: ..."""
    # TODO: Imp pathlib throughout, for crossplatform (win, mac)
    def __init__(self, root):
        self.root = pathlib.Path(root)

        # TODO: imp file, folder checking.
        self.IGNORED = ['visualhouse', '1 From AWS', 'Thumbs.db', '.DS_Store']


    def _string_builder(self, args):
        """builds directory from a list of strings"""
        # TODO: pathlib for crossplatform support.
        _str = ''
        for loc in args:
            _str = f'{_str}\\{loc}'
            
        return _str


    def dir_from_root(self, *args):
        # TODO: self.root doesnt seem to be escaping \\
        # slicing string as WORKAROUND.
        return f'{str(self.root)[:-1]}{self._string_builder(args)}'


    def get_clients(self):
        """get all client folders from self.root
        Return: List: ['client', 'client', 'client']"""
        # TODO: imp file, folder checking
        result = []
        clients = os.listdir(self.root)
        
        for client in clients:
            if os.path.isdir(f'{self.root}{client}'):
                result.append(client)

        return sorted(result)


    def get_projects(self, client):
        """get all projects under client.
        AUG:
        client: str: client name.
        Return: list: ['project', 'project', 'project', ]"""
        # TODO: imp file, folder checking
        result = []
        projects = pathlib.Path(self.root, client)
        
        for item in os.listdir(projects):
            if pathlib.Path(projects, item).is_dir():
                result.append(item)

        return result


    def create_folder(self, folder_name):
        """creates all folders that dont exist in folder_name"""
        # TODO: refactor to self.create_path
        project_drive = pathlib.Path(self.root)
        if len(folder_name) > 0:
            if project_drive.is_dir():
                new_dir = project_drive / folder_name
                if new_dir.is_dir():
                    pass
                else:
                    new_dir.mkdir()


    def create_path(self, string_path):
        """creates all folders that dont exist in folder_name
        string_path: str repr of path, sep with double forward slash"""
        path = pathlib.Path(self.root, string_path)
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)


    def get_projects_and_jobs(self, client):
        """retrieves all of a clients projects and tasks.
        client: str: name of client as written in directory.
        return: dict: {'project_name': ['job', 'job', 'job']}"""
        # TODO: imp file, folder checking
        client_dir = f'{self.root}{client}'
        projects = os.listdir(client_dir)
        projects_and_jobs = {}

        for project in projects:
            project_dir = f'{client_dir}\\{project}'
            if os.path.isdir(project_dir):
                projects_and_jobs[project] = [
                    x for x in os.listdir(project_dir) if os.path.isdir(f'{project_dir}\\{x}')
                ]

        return projects_and_jobs


    def get_issues_files(self, client_name, project_name, job_name):
        """retrieves all of a jobs issued information.
        client_name: str: name of client as written in directory.
        project_name: str: name of project as written in directory.
        job_name: str: name of job as written in directory.
        return: dict: {'issue_folder': ['issue', 'issue', 'issue']}"""
        # TODO: imp file, folder checking
        issued_dir = self.dir_from_root(
            client_name, project_name, job_name, 'Support', 
            'Issued Information'
        )
        result = {}

        for issued_folder in os.listdir(issued_dir):
            if issued_folder not in result and os.path.isdir(issued_folder):
                result[issued_folder] = os.listdir(
                    f'{issued_dir}\\{issued_folder}'
                )

        return result


    def get_master_files(self, client_name, project_name, job_name):
        """gets all names of files from a still project Master folder
        return: list: ['file', 'file', 'file']"""
        # TODO: imp file/folder checking
        master_folder_dir = self.dir_from_root(
            client_name, project_name, job_name, 'Still & Film', 
            'Max Files', 'Still Imagery', 'Master'
        )
        
        return os.listdir(master_folder_dir)


    def get_scene_files(self, client_name, project_name, job_name):
        """gets all names of files from a still project Scene folder
        return: list: ['file', 'file', 'file']"""
        # TODO: imp file/folder checking
        self.dir_from_root(client_name, project_name, job_name, )
        scene_folder_dir = self.dir_from_root(
            client_name, project_name, job_name, 'Still & Film', 
            'Max Files', 'Still Imagery', 'Scene'
        )

        return os.listdir(scene_folder_dir)


class OsOpen():
    # TODO: use pathlib for crossplatform, (win, mac)
    def __init__(self, location):
        self.location = location
        self._dir, self._filename = os.path.split(location)

        if not os.path.isdir(os.path.split(location)[0]):
            # TODO: raise error
            print('path does not exist')
        else:
            self._dir = os.path.split(location)[0]

        if not not os.path.isdir(os.path.split(location)[1]):
            self._filename = None
        else:
            self._filename = os.path.split(location)[1]


    def open(self):
        """decides wether to open a file or directory"""
        if self._filename:
            os.startfile(f'{self._dir}\\{self._filename}')
        else:
            os.startfile(self._dir)
