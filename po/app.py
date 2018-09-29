import sys
 
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import (
    QApplication, QPushButton, QLineEdit, QListWidget, QTreeWidget, 
    QTreeWidgetItem, QGroupBox, QTabWidget, QPushButton
)
from PySide2.QtCore import QFile, QObject

from modules import io
 

# TODO: figure out multiple forms? settings form for instance
# TODO: figure out how to check if the client..project..job file 
# struture is correct?


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
        self.project_root = "d:\\"

        # widgets
        self.client_list = self.window.findChild(QListWidget, 'client_list')
        self.project_tree = self.window.findChild(QTreeWidget, 'project_tree')
        self.issued_tree = self.window.findChild(QTreeWidget, 'issued_tree')
        self.master_list = self.window.findChild(QListWidget, 'master_files')
        self.scene_list = self.window.findChild(QListWidget, 'scene_files')
        self.fs_ref = self.window.findChild(QPushButton, 'fs_ref')
        self.fs_photography = self.window.findChild(QPushButton, 'fs_photography')
        self.fs_artdirection = self.window.findChild(QPushButton, 'fs_artdirection')
        self.fs_render = self.window.findChild(QPushButton, 'fs_render')

        # groups
        self.project_job_groupbox = self.window.findChild(QGroupBox, 'project_job_groupbox')
        self.hide(self.project_job_groupbox)
        self.folder_shortcuts = self.window.findChild(QGroupBox, 'folder_shortcuts')
        self.hide(self.folder_shortcuts)
        self.tabWidget = self.window.findChild(QTabWidget, 'tabWidget')
        self.hide(self.tabWidget)

        # widget actions
        self.client_list.itemSelectionChanged.connect(self.action_client_list_changed)
        self.project_tree.itemSelectionChanged.connect(self.action_project_tree_changed)
        self.issued_tree.itemSelectionChanged.connect(self.action_issued_tree_changed)
        self.master_list.itemSelectionChanged.connect(self.action_master_tree_changed)
        self.fs_ref.clicked.connect(self.clicked_fs_ref)
        self.fs_photography.clicked.connect(self.clicked_fs_photography)
        self.fs_render.clicked.connect(self.clicked_fs_render)

        # start up
        self.get_clients()
        self.window.show()


    # utility
    def hide(self, widget):
        """hides a widget"""
        widget.close()


    def show(self, widget):
        """shows a widget"""
        widget.show()


    # widget actions
    def action_client_list_changed(self):
        """logic to run when user selects a Client"""
        self.project_tree.clear()

        client = self.client_list.currentItem().text()

        self.hide(self.folder_shortcuts)
        self.hide(self.tabWidget)

        self.show(self.project_job_groupbox)

        return self.update_project_tree(client)


    def action_project_tree_changed(self):
        """logic to run when user selects a project/job"""
        self.master_list.clear()
        self.scene_list.clear()
        self.issued_tree.clear()

        client = self.client_list.currentItem().text()
        
        if self.project_tree.currentItem().parent():
            project = self.project_tree.currentItem().parent().text(0)
            job = self.project_tree.currentItem().text(0)

            master_files_names = io.Manager(self.project_root).get_master_files(client, project, job)
            scene_files_names = io.Manager(self.project_root).get_scene_files(client, project, job)
            self.update_issued_tree(job)
            self.update_master_tree(master_files_names)
            self.update_scene_tree(scene_files_names)

            self.show(self.folder_shortcuts)
            self.show(self.tabWidget)

            return True

        else:
            print('parent')

            self.hide(self.folder_shortcuts)
            self.hide(self.tabWidget)


    def action_issued_tree_changed(self):
            """checks wether or not the selected item is a file and runs it."""
            client = self.client_list.currentItem().text()
            project = self.project_tree.currentItem().parent().text(0)

            if self.issued_tree.currentItem().parent():
                job = self.project_tree.currentItem().text(0)
                issue_folder = self.issued_tree.currentItem().parent().text(0)

                issue_file_loc = io.Manager(self.project_root).dir_from_root(
                    client, project, job, 'Support', 'Issued Information', 
                    issue_folder, self.issued_tree.currentItem().text(0)
                    )

                io.OsOpen(issue_file_loc).open()
            
            else:
                pass


    def action_master_tree_changed(self):
        client = self.client_list.currentItem().text()
        job = self.project_tree.currentItem().text(0)

        if self.project_tree.currentItem().parent():
            project = self.project_tree.currentItem().parent().text(0)

            master_file_loc = io.Manager(self.project_root).dir_from_root(
                    client, project, job, 'Still & Film', 'Max Files', 
                    'Still Imagery', 'Master', 
                    self.master_list.currentItem().text()
            )

            io.OsOpen(master_file_loc).open()
        
        else:
            pass


    def clicked_fs_ref(self):
        client = self.client_list.currentItem().text()
        project = self.project_tree.currentItem().parent().text(0)
        job = self.project_tree.currentItem().text(0)

        ref_folder_dir = io.Manager(self.project_root).dir_from_root(
            client, project, job, 'Support', 'Reference Imagery'
        )
        io.OsOpen(ref_folder_dir).open()


    def clicked_fs_photography(self):
        client = self.client_list.currentItem().text()
        project = self.project_tree.currentItem().parent().text(0)
        job = self.project_tree.currentItem().text(0)

        photography_loc = io.Manager(self.project_root).dir_from_root(
            client, project, job, 'Support', 'Photography'
        )
        io.OsOpen(photography_loc).open()


    def clicked_fs_render(self):
        client = self.client_list.currentItem().text()
        project = self.project_tree.currentItem().parent().text(0)
        job = self.project_tree.currentItem().text(0)

        render_loc = io.Manager(self.project_root).dir_from_root(
            client, project, job, 'Still & Film', 'Renders'
        )
        io.OsOpen(render_loc).open()


    # functions
    def get_clients(self):
        """appends list of clients to client_list"""
        clients = io.Manager(self.project_root).get_clients()
        
        for client in clients:
            self.client_list.addItem(client)


    def update_project_tree(self, client_name):
        """updates the project tree, when a new client is selected"""
        self.project_tree.clear()
        self.issued_tree.clear()

        t = io.Manager(self.project_root).get_projects_and_jobs(client_name)

        for key, value in t.items():
            root = QTreeWidgetItem(self.project_tree, [key])

            for val in value:
                item = QTreeWidgetItem([val])
                root.addChild(item)

        return t


    def update_issued_tree(self, job):
        """updates the issued tree, when a new project/job is selected"""
        self.issued_tree.clear()

        client = self.client_list.currentItem().text()
        project = self.project_tree.currentItem().parent().text(0)
        issues_dict = io.Manager(self.project_root).get_issues_files(client, project, job)

        for issue_folder, issues in issues_dict.items():
            root = QTreeWidgetItem(self.issued_tree, [issue_folder])

            if len(issues) > 0:
                for val in issues:
                    item = QTreeWidgetItem([val])
                    root.addChild(item)


    def update_master_tree(self, files):
        self.master_list.clear()
        for file in files:
            self.master_list.addItem(file)


    def update_scene_tree(self, files):
        self.scene_list.clear()
        for file in files:
            self.scene_list.addItem(file)

 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form('main.ui')
    sys.exit(app.exec_())