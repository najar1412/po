import sys
 
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton, QLineEdit, QListWidget, QTreeWidget, QTreeWidgetItem
from PySide2.QtCore import QFile, QObject

from modules import folder
 

 # TODO: figure out multiple forms? settings form for instance
 # TODO: open files (issues)
 # TODO: impl folder shortcuts
 # TODO: figure out how to check if the client..project..job file 
 # #struture is correct? and to know display them?

class Form(QObject):
    """qt form"""
    def __init__(self, ui_file, parent=None):
        super(Form, self).__init__(parent)

        # settings
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()

        # globals
        self.project_root = 'd:\\'
        self.PROJECT = ''
        self.CLIENT = ''
        self.JOB = ''
        self.ISSUE = ''

        # widgets
        self.client_list = self.window.findChild(QListWidget, 'client_list')
        self.project_tree = self.window.findChild(QTreeWidget, 'project_tree')
        self.issued_tree = self.window.findChild(QTreeWidget, 'issued_tree')
        self.master_tree = self.window.findChild(QListWidget, 'master_files')
        self.scene_tree = self.window.findChild(QListWidget, 'scene_files')

        # widget actions
        self.client_list.itemSelectionChanged.connect(self.action_client_list_changed)
        self.project_tree.itemSelectionChanged.connect(self.action_project_tree_changed)
        self.issued_tree.itemSelectionChanged.connect(self.action_issued_tree_changed)

        # start up logic
        self.get_clients()
        self.window.show()


    def get_clients(self):
        """appends list of clients to client_list"""
        clients = folder.Manager(self.project_root).get_clients()
        
        for client in clients:
            self.client_list.addItem(client)


    def action_client_list_changed(self):
        """logic to run when user selects a Client"""
        self.project_tree.clear()
        self.CLIENT = self.client_list.currentItem().text()

        return self.update_project_tree(self.CLIENT)


    def action_project_tree_changed(self):
        """logic to run when user selects a project/job"""
        self.CLIENT = self.client_list.currentItem().text()
        projects = folder.Manager(self.project_root).get_projects_and_jobs(self.CLIENT)
        project_selection = self.project_tree.selectedItems()

        if project_selection:
            selection_name = project_selection[0].text(0)

            if selection_name not in projects:
                self.JOB = selection_name
                master_files_names = folder.Manager(self.project_root).get_master_files(self.CLIENT, self.PROJECT, self.JOB)
                scene_files_names = folder.Manager(self.project_root).get_scene_files(self.CLIENT, self.PROJECT, self.JOB)
                self.update_issued_tree(self.JOB)
                self.update_master_tree(master_files_names)
                self.update_scene_tree(scene_files_names)

                return selection_name

            else:
                self.PROJECT = selection_name

        return False


    def action_issued_tree_changed(self):
            """checks wether or not the selected item is a file and runs it."""
            client = self.client_list.currentItem().text()
            project = self.project_tree.currentItem().parent().text(0)

            if self.issued_tree.currentItem().parent():
                job = self.issued_tree.currentItem().parent().text(0)

                lissue_file_loc = folder.Manager(self.project_root).dir_from_root(
                    client, project, job, 'Support', 'Issued Information', 
                    self.issued_tree.currentItem().text(0)
                    )

                folder.OpenFile(f'"{lissue_file_loc}"').open()
            
            else:
                pass


    def update_project_tree(self, client_name):
        """updates the project tree, when a new client is selected"""
        self.project_tree.clear()
        self.issued_tree.clear()

        t = folder.Manager(self.project_root).get_projects_and_jobs(client_name)

        for key, value in t.items():
            root = QTreeWidgetItem(self.project_tree, [key])

            for val in value:
                item = QTreeWidgetItem([val])
                root.addChild(item)

        return t


    def update_issued_tree(self, job):
        """updates the issued tree, when a new project/job is selected"""
        self.issued_tree.clear()

        client_name = self.client_list.currentItem().text()
        t = folder.Manager(self.project_root).get_issues_files(client_name, self.PROJECT, job)

        for key, value in t.items():
            root = QTreeWidgetItem(self.issued_tree, [key])

            if len(value) > 0:
                for val in value:
                    item = QTreeWidgetItem([val])
                    root.addChild(item)

        return True


    def update_master_tree(self, files):
        self.master_tree.clear()
        for file in files:
            self.master_tree.addItem(file)

        return True


    def update_scene_tree(self, files):
        self.scene_tree.clear()
        for file in files:
            self.scene_tree.addItem(file)

        return True
 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form('main.ui')
    sys.exit(app.exec_())