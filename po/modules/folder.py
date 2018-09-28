import pathlib
import os

# scan project dir
# report directors over the standard windows dir length
# make project folders
# display drive projects
# archive project

class Manager():
    """tools built around default project structure"""
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
        return f'{self.root}{self._string_builder(args)}'


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
                    x for x in os.listdir(project_dir)
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
            if issued_folder not in result:
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


class OpenFile():
    def __init__(self, location):
        self.location = location

    def open(self):
        os.system(f'start {self.location}')

    def test(self):
        print(self.location)
        print('testing fine!')
        

# old, could be helpful code
class ProjectMan():
    """tools built around default project structure"""
    def __init__(self, project_root):
        """project_root: str: repr root folder of projects"""
        self.root = pathlib.Path(project_root)

        self.IGNORED = ['visualhouse', '1 From AWS', 'Thumbs.db', '.DS_Store']

    
    def _max_path_safe(self, directory):
        """checks if the full directory exceces """
        if len(directory) >= 240:
            return False
        else:
            return True
        

    def walk_project(self, project_name):
        """recursively walks directories.
        project_name: str: name of the folder to walk
        return: dict: {'directory': ['folders': [], 'files': []]}"""
        project = {}
        for (dirpath, dirnames, filenames) in os.walk(pathlib.Path(self.root, project_name)):
            if dirpath not in project:
                project[dirpath] = {'folders': dirnames, 'files': filenames}

        return project


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
                    x for x in os.listdir(project_dir)
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
            if issued_folder not in result:
                result[issued_folder] = os.listdir(
                    f'{issued_dir}\\{issued_folder}'
                )

        return result


    def _string_builder(self, args):
        _str = ''
        for loc in args:
            _str = f'{_str}\\{loc}'
        
        return _str


    def dir_from_root(self, *args):
        return f'{self.root}{self._string_builder(args)}'
        

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


    def project_checker(self, project_name):
        details = {
            'folders': 0,
            'files': 0,
            'error_max_length_count': 0,
            'error_max_length': [],
            }

        project = self.walk_project(project_name)

        for directory in project.keys():
            if not self._max_path_safe(directory):
                details['error_max_length'].append(directory)

            if project[directory]:
                details['folders'] += len(project[directory]['folders'])
                details['files'] += len(project[directory]['files'])

        details['error_max_length_count'] = len(details['error_max_length'])

        return details
