import pathlib
import os

# scan project dir
# report directors over the standard windows dir length
# make project folders
# display drive projects
# archive project

class ProjectMan():
    """reports of project structure"""
    def __init__(self, project_root):
        """project_root: str: repr root folder of projects"""
        self.project_root = pathlib.Path(project_root)

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
        for (dirpath, dirnames, filenames) in os.walk(pathlib.Path(self.project_root, project_name)):
            if dirpath not in project:
                project[dirpath] = {'folders': dirnames, 'files': filenames}

        return project


    def walk_clients(self):
        """HELPER: Scans project drive
        Return: List: clients and developers
        """
        folders = []
        clients = os.listdir(self.project_root)

        for item in clients:
            if os.path.isdir(f'{self.project_root}{item}') and not item.startswith('.') and not item.startswith('#') and item not in self.IGNORED:
                folders.append(item)

        return sorted(folders)


    def walk_client_projects(self, client_name):
        folders = []
        client_dir = f'{self.project_root}{client_name}'
        client_folders = os.listdir(client_dir)
        projects_issued = {}

        for project in client_folders:
            if os.path.isdir(client_dir) and not project.startswith('.') and not project.startswith('#') and project not in self.IGNORED:
                folders.append(project)

                if project not in projects_issued:
                    projects_issued[project] = []

                projects_issued[project] = [x for x in os.listdir(f'{client_dir}\\{project}') if x not in self.IGNORED]


        return projects_issued


    def walk_client_project_issued(self, client_name, project_name, job_name):
        project_dir = f'{self.project_root}{client_name}\\{project_name}\\{job_name}'
        project_folders = os.listdir(project_dir)
        result = {}

        for folder in project_folders:
            if folder.lower() == 'support':
                project_issued_information = f'{project_dir}\\{folder}\\Issued Information'
                issued_dir = os.listdir(project_issued_information)

                for issued in issued_dir:
                    if issued not in result and issued not in self.IGNORED:
                        result[issued] = os.listdir(f'{project_issued_information}\\{issued}')

        return result


    def walk_client_project_masters(self, client_name, project_name, job_name):
        master_dir = f'{self.project_root}{client_name}\\{project_name}\\{job_name}\\Still & Film\\Max Files\\Still Imagery\\Master'
        master_folders = os.listdir(master_dir)

        return master_folders


    def walk_client_project_scenes(self, client_name, project_name, job_name):
        master_dir = f'{self.project_root}{client_name}\\{project_name}\\{job_name}\\Still & Film\\Max Files\\Still Imagery\\Scene'
        master_folders = os.listdir(master_dir)

        return master_folders


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