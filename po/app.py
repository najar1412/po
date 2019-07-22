__author__ = 'Rory Jarrel'
__version__ = '2019.0.1'

# TODO: is folder struture is correct?
# TODO: after creating a new client, project, job. Select the newly creted 
# thing.

import sys
import os
 
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import (
    QApplication, QPushButton, QLineEdit, QListWidget, QTreeWidget, 
    QTreeWidgetItem, QGroupBox, QTabWidget, QPushButton, QComboBox,
    QAction, QMenu, QVBoxLayout, QSystemTrayIcon, QFileDialog, QListWidgetItem
)
from PySide2.QtCore import QFile, QObject
from PySide2.QtGui import QIcon
#  WORKAROUND: below import is for pyinstaller to know where the module is.
# isnt actually used...
from PySide2.QtXml import QDomNode

from modules import io, folder, project_scanner, aws


# Used for location UIs and other graphics. _MEIPASS will only be in `sys`
# the app has been packaged using `pyinstaller _app.spec`
if hasattr(sys, '_MEIPASS'):
    main_res = os.path.join(sys._MEIPASS, "main_res.ui")
    new_client_dialog = os.path.join(sys._MEIPASS, "new_client_dialog.ui")
    new_job_dialog = os.path.join(sys._MEIPASS, "new_job_dialog.ui")
    new_project_dialog = os.path.join(sys._MEIPASS, "new_project_dialog.ui")
    project_checker_dialog = os.path.join(sys._MEIPASS, "project_checker_dialog.ui")
    settings_dialog = os.path.join(sys._MEIPASS, "settings_dialog.ui")
    project_upload_dialog = os.path.join(sys._MEIPASS, "project_upload_dialog.ui")

    heart_artwork = os.path.join(sys._MEIPASS, "heart.png")
else:
    main_res = "D:\code\po\po\\main_res.ui"
    new_client_dialog = "D:\code\po\po\\new_client_dialog.ui"
    new_job_dialog = "D:\code\po\po\\new_job_dialog.ui"
    new_project_dialog = "D:\code\po\po\\new_project_dialog.ui"
    project_checker_dialog = "D:\code\po\po\\project_checker_dialog.ui"
    settings_dialog = "D:\code\po\po\\settings_dialog.ui"
    project_upload_dialog = "D:\code\po\po\\project_upload_dialog.ui"

    heart_artwork = "D:\code\po\po\\artwork\heart.png"

# CONFIG
class Config():
    def __init__(self):
        self.project_drive = 'z:\\'


    def _update_project_drive(self, letter):
        windows_req = ':\\'
        self.project_drive = f'{letter}{windows_req}'

        return self.project_drive


    def fetch_drive(self):
        return self.project_drive


# HELPERS
OFFICES = {'New York': 'nyarchive', 'London': '', 'Los Angeles': ''}
class Helpers():
    """Collection of helper functions, usually used for passing widgets between 
    dialogs"""
    def __init__(self, widgets=None, data=None):
        if widgets and 'hide' in widgets:
            self.hide_widgets = widgets['hide']
        else:
            self.hide_widgets = None
        if widgets and 'clear' in widgets:
            self.clear_widgets = widgets['clear']
        else:
            self.clear_widgets = None
        if data:
            self.data = data
        else:
            self.data = None
        
        
    def window_refresh(self):
        """hides and clears any number widgets and re-populates.

        self.data is used to populate cleared widgets, accepts a list:
        First element is the function to call to populate.
        Second element is any augment used to call the function.

            i.e. update_project_tree function needs a client name in order
                to populate."""
        if self.hide_widgets:
            for widget in self.hide_widgets:
                widget.hide()
        if self.clear_widgets:
            for widget in self.clear_widgets:
                widget.clear()
        if self.data:
            if len(self.data) > 1:
                func = self.data[0]
                func(self.data[1])
            else:
                func = self.data[0]
                func()

        return True


def bg_thread():
    # TODO: imp new thread for running tasks in cmd, in the BG.
    return False

# DIALOGS
class NewClientDialog(QObject):
    def __init__(self, ui_file, config, clients=None, parent=None, helper=None):

        # globals
        self.project_root = config.project_drive

        # UI
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()

        if clients:
            self.clients = clients
        if helper:
            self.helper = helper

        # widgets
        self.pb_save = self.window.findChild(QPushButton, 'pb_save')
        self.pb_discard = self.window.findChild(QPushButton, 'pb_discard')
        self.cb_client_list = self.window.findChild(QComboBox, 'cb_client_list')

        self.le_client_name = self.window.findChild(QLineEdit, 'le_client_name')

        # actions
        self.pb_save.clicked.connect(self.clicked_pb_save)
        self.pb_discard.clicked.connect(self.clicked_pb_discard)

        # mmm
        if clients:
            for client in clients['data']:
                self.cb_client_list.addItem(client)
                
            client_index = self.cb_client_list.findText(clients['selected'])
            if client_index >= 0:
                self.cb_client_list.setCurrentIndex(client_index)

        self.window.show()

    
    def clicked_pb_save(self):
        client_name = self.le_client_name.text()
        io.Manager(self.project_root).create_folder(client_name)

        self.window.close()
        self.helper.window_refresh()

    
    def clicked_pb_discard(self):
        self.window.close()


class ProjectCheckerDialog(QObject):
    # TODO: if user changes client during making a new job, the 
    # project list should update to the new client
    # TODO: on creating a new job strut projects window needs to refresh
    def __init__(self, ui_file, config):
        self.config = config
        # UI
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()

        # widgets
        self.le_project_scan = self.window.findChild(QPushButton, 'le_project_scan')
        self.project_tree = self.window.findChild(QTreeWidget, 'project_tree')
        self.main_layout = self.window.findChild(QVBoxLayout, 'verticalLayout')
        self.project_tree.hide()

        # actions
        self.le_project_scan.clicked.connect(self.clicked_le_project_scan)
        self.project_tree.itemSelectionChanged.connect(self.action_project_tree_changed)
        
        self.window.show()


    # action functions
    def clicked_le_project_scan(self):
        # TODO: refresh project_job_list after adding a new project
        projects = project_scanner.get_folders(self.config.fetch_drive())
        for project in projects:
            bad_project = project_scanner.run_report(project)
            if bad_project:
                self.update_project_checker_tree(bad_project)


    def action_project_tree_changed(self):
            """opens selected folder"""

            if self.project_tree.currentItem().parent():
                io.OsOpen(self.project_tree.currentItem().text(0)).open()
            
            else:
                pass


    # functions
    def update_project_checker_tree(self, projects):
        """updates the project tree, when a new client is selected"""
        self.project_tree.show()
        for key, value in projects.items():
            root = QTreeWidgetItem(self.project_tree, [f'{key} ({len(value)} issues)'])

            for val in value:
                item = QTreeWidgetItem([val])
                root.addChild(item)

        return True


class NewJobDialog(QObject):
    # TODO: if user changes client during making a new job, the 
    # project list should update to the new client
    # TODO: on creating a new job strut projects window needs to refresh
    def __init__(self, ui_file, config, clients=None, projects=None, parent=None, helper=None):
        # UI
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()

        if clients:
            self.clients = clients

        if projects:
            self.projects = projects

        # globals
        self.project_root = config.project_drive
        if helper:
            self.helper = helper

        # widgets
        self.pb_save = self.window.findChild(QPushButton, 'pb_save')
        self.pb_discard = self.window.findChild(QPushButton, 'pb_discard')
        self.cb_client_list = self.window.findChild(QComboBox, 'cb_client_list')
        self.cb_project_list = self.window.findChild(QComboBox, 'cb_project_list')
        self.le_job_number = self.window.findChild(QLineEdit, 'le_job_number')
        self.le_job_desc = self.window.findChild(QLineEdit, 'le_job_desc')

        # actions
        self.pb_save.clicked.connect(self.clicked_pb_save)
        self.pb_discard.clicked.connect(self.clicked_pb_discard)

        # populate
        if clients:
            for client in clients['data']:
                self.cb_client_list.addItem(client)
                
            client_index = self.cb_client_list.findText(clients['selected'])
            if client_index >= 0:
                self.cb_client_list.setCurrentIndex(client_index)

        if projects:
            for project in projects['data']:
                self.cb_project_list.addItem(project)
                
            project_index = self.cb_project_list.findText(projects['selected'])
            if project_index >= 0:
                self.cb_project_list.setCurrentIndex(project_index)

        self.window.show()

    
    def clicked_pb_save(self):
        # client_name = self.le_client_name.text()

        data = {
            'client': self.cb_client_list.currentText(),
            'project': self.cb_project_list.currentText(),
            'job_number': self.le_job_number.text(),
            'job_desc': self.le_job_desc.text()
        }

        folder.build_job(self.project_root, data['client'], data['project'], f"JC001-{data['job_number']}-{data['job_desc']}")

        # io.Manager(self.project_root).create_folder(client_name)

        self.window.close()
        self.helper.window_refresh()

    
    def clicked_pb_discard(self):
        self.window.close()


class NewProjectDialog(QObject):
    def __init__(self, ui_file, config, clients=None, parent=None, helper=None):

        # UI
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()

        if clients:
            self.clients = clients

        # globals
        self.project_root = config.project_drive
        if helper:
            self.helper = helper

        # widgets
        self.pb_save = self.window.findChild(QPushButton, 'pb_save')
        self.pb_discard = self.window.findChild(QPushButton, 'pb_discard')
        self.cb_client_list = self.window.findChild(QComboBox, 'cb_client_list')
        self.le_project_code = self.window.findChild(QLineEdit, 'le_project_code')
        self.le_project_iter = self.window.findChild(QLineEdit, 'le_project_iter')
        self.le_project_name = self.window.findChild(QLineEdit, 'le_project_name')
        self.le_project_loc = self.window.findChild(QLineEdit, 'le_project_loc')


        # actions
        self.pb_save.clicked.connect(self.clicked_pb_save)
        self.pb_discard.clicked.connect(self.clicked_pb_discard)

        # mmm
        if clients:
            for client in clients['data']:
                self.cb_client_list.addItem(client)
                
            client_index = self.cb_client_list.findText(clients['selected'])
            if client_index >= 0:
                self.cb_client_list.setCurrentIndex(client_index)

        self.window.show()

    
    def clicked_pb_save(self):
        # TODO: refresh project_job_list after adding a new project
        data = {
            'client': self.cb_client_list.currentText(),
            'project_code': [self.le_project_code.text(), self.le_project_iter.text()],
            'project_name': self.le_project_name.text(),
            'project_loc': self.le_project_loc.text()
        }

        path = f"{data['client']}//{data['project_code'][0]}{data['project_code'][1]}-{data['project_name']},{data['project_loc']}"
        io.Manager(self.project_root).create_path(path)

        self.window.close()
        self.helper.window_refresh()

    
    def clicked_pb_discard(self):
        self.window.close()


class SettingsDialog(QObject):
    def __init__(self, ui_file, config, clients=None, parent=None, helper=None):

        # UI
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()

        self.window.show()


class ProjectUploadDialog(QObject):
    # TODO: Disable upload button until Project folder and selected office have
    # been done.
    def __init__(self, ui_file, config, clients=None, parent=None, helper=None):
        # UI
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()

        self.project_dir = 'Select a Project Folder...'
        self.bucket = None

        # widgets
        self.pb_upload_archive = self.window.findChild(QPushButton, 'pb_uploadArchive')
        self.pb_select_dir = self.window.findChild(QPushButton, 'pb_selectDir')
        self.le_project_folder = self.window.findChild(QLineEdit, 'le_project_folder')
        self.cb_office = self.window.findChild(QComboBox, 'cb_office')
        self.gb_files_to_upload = self.window.findChild(QGroupBox, 'gb_filesToUpload')
        self.gb_files_to_upload.hide()
        self.lw_files_to_upload = self.window.findChild(QListWidget, 'lw_filesToUpload')

        # Widget Defaults
        self.le_project_folder.setText(self.project_dir)

        # actions
        self.pb_upload_archive.clicked.connect(self.clicked_pb_upload_archive)
        self.pb_select_dir.clicked.connect(self.clicked_pb_select_dir)
        self.cb_office.activated.connect(self.clicked_cb_office)

        self.window.show()

    # HELPERS
    def get_archives(self):
        archives = []
        for f in os.listdir(self.project_dir):
            if os.path.splitext(f)[1] == '.zip' or os.path.splitext(f)[1] == '.rar':
                archives.append(f)

        return archives

    
    def add_items_to_upload(self):
        for i in self.get_archives():
            item = QListWidgetItem(i)
            self.lw_files_to_upload.addItem(item)


    def clicked_pb_upload_archive(self):
        # TODO: Open new cmd in a different thread
        # TODO: send commands to new cmd using user entered data
        # TODO: on upload completion, notify gui
        # s3uri = 's3://nyarchive/test_client/test_project/'
        
        aws.run_upload(self.bucket, self.project_dir)


    def clicked_pb_select_dir(self):
        fname = QFileDialog.getExistingDirectory()
        self.project_dir = fname
        self.le_project_folder.setText(self.project_dir)
        self.add_items_to_upload()
        self.gb_files_to_upload.show()


    def clicked_cb_office(self):
        selected_office = self.cb_office.currentText()
        if selected_office in OFFICES:
            self.bucket = OFFICES[selected_office]


class MainWindow(QObject):
    """qt form"""
    def __init__(self, ui_file, config, parent=None):
        super(MainWindow, self).__init__(parent)

        # settings
        self.config = config
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()

        # globals
        self.project_root = config.project_drive

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
        self.pb_project_drive = self.window.findChild(QPushButton, 'pb_project_drive')
        self.le_project_drive = self.window.findChild(QLineEdit, 'le_project_drive')
        self.le_project_drive.setPlaceholderText = self.project_root
        self.pb_new_client = self.window.findChild(QPushButton, 'pb_new_client')
        self.pb_refresh = self.window.findChild(QPushButton, 'pb_refresh')
        self.pb_new_project = self.window.findChild(QPushButton, 'pb_new_project')
        self.pb_new_job = self.window.findChild(QPushButton, 'pb_new_job')
        self.pb_deliver = self.window.findChild(QPushButton, 'pb_deliver')
        # Menu > Tools
        self.submenu_settings = self.window.findChild(QAction, 'actionSettings')
        # Menu > Archival
        self.menu_project_checker = self.window.findChild(QAction, 'actionProject_Checker')
        self.menu_project_upload = self.window.findChild(QAction, 'actionProject_Upload')

        # groups
        self.project_job_groupbox = self.window.findChild(QGroupBox, 'project_job_groupbox')
        self.hide(self.project_job_groupbox)
        self.folder_shortcuts = self.window.findChild(QGroupBox, 'folder_shortcuts')
        self.hide(self.folder_shortcuts)
        self.gb_job_info = self.window.findChild(QGroupBox, 'gb_job_information')
        self.hide(self.gb_job_info)

        # widget actions
        self.client_list.itemSelectionChanged.connect(self.action_client_list_changed)
        self.project_tree.itemSelectionChanged.connect(self.action_project_tree_changed)
        self.issued_tree.itemSelectionChanged.connect(self.action_issued_tree_changed)
        self.master_list.itemSelectionChanged.connect(self.action_master_tree_changed)
        self.fs_ref.clicked.connect(self.clicked_fs_ref)
        self.fs_photography.clicked.connect(self.clicked_fs_photography)
        self.fs_render.clicked.connect(self.clicked_fs_render)
        self.pb_project_drive.clicked.connect(self.clicked_pb_project_drive)
        self.pb_new_client.clicked.connect(self.clicked_pb_new_client)
        self.pb_refresh.clicked.connect(self.clicked_pb_refresh)
        self.pb_new_project.clicked.connect(self.clicked_pb_new_project)
        self.pb_new_job.clicked.connect(self.clicked_pb_new_job)
        self.pb_deliver.clicked.connect(self.clicked_pb_deliver)
        self.menu_project_checker.triggered.connect(self.clicked_menu_project_checker)
        self.menu_project_upload.triggered.connect(self.clicked_menu_project_upload)
        self.submenu_settings.triggered.connect(self.clicked_submenu_settings)

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
        self.hide(self.gb_job_info)

        self.show(self.project_job_groupbox)
        self.hide(self.pb_new_job)

        return self.update_project_tree(client)


    def action_project_tree_changed(self):
        """logic to run when user selects a project/job"""
        self.master_list.clear()
        self.scene_list.clear()
        self.issued_tree.clear()

        client = self.client_list.currentItem().text()
        self.show(self.pb_new_job)
        
        if self.project_tree.currentItem().parent():
            project = self.project_tree.currentItem().parent().text(0)
            job = self.project_tree.currentItem().text(0)

            master_files_names = io.Manager(self.project_root).get_master_files(client, project, job)
            scene_files_names = io.Manager(self.project_root).get_scene_files(client, project, job)
            self.update_issued_tree(job)
            self.update_master_tree(master_files_names)
            self.update_scene_tree(scene_files_names)

            self.show(self.folder_shortcuts)
            self.show(self.gb_job_info)

            return True

        else:
            self.hide(self.folder_shortcuts)
            self.hide(self.gb_job_info)


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


    def clicked_pb_project_drive(self):
        self.project_root = self.config._update_project_drive(self.le_project_drive.text())

        self.client_list.clear()
        self.hide(self.project_job_groupbox)
        self.project_tree.clear()
        
        self.get_clients()


    def clicked_pb_new_client(self):
        # TODO: figure how to refresh the client list once a new folder has been added.
        widgets = {'hide': [self.project_job_groupbox], 'clear': [self.project_tree, self.client_list]}
        helper = Helpers(widgets=widgets, data=[self.get_clients])

        self.dialog = NewClientDialog(new_client_dialog, default_config, helper=helper)


    def clicked_pb_refresh(self):
        self.hide(self.project_job_groupbox)
        self.project_tree.clear()
        self.client_list.clear()

        self.get_clients()
        print('refreshing...')


    def clicked_pb_new_project(self):
        clients = io.Manager(self.project_root).get_clients()
        selected_client = self.client_list.currentItem().text()
        clients = {
            'selected': selected_client, 
            'data': clients
        }

        helper = Helpers(data=[self.update_project_tree, selected_client])

        self.dialog = NewProjectDialog(new_project_dialog, default_config, clients=clients, helper=helper)


    def clicked_pb_new_job(self):
        clients = {
            'selected': self.client_list.currentItem().text(), 
            'data': io.Manager(self.project_root).get_clients()
        }

        projects = {'selected': '', 'data': ''}

        if self.project_tree.currentItem().parent():
            selected = self.project_tree.currentItem().parent().text(0)
            projects['selected'] = selected
            projects['data'] = io.Manager(self.project_root).get_projects(clients['selected'])

        else:
            selected = self.project_tree.currentItem().text(0)
            projects['selected'] = selected
            projects['data'] = io.Manager(self.project_root).get_projects(clients['selected'])

        helper = Helpers(data=[self.update_project_tree, clients['selected']])

        self.dialog = NewJobDialog(new_job_dialog, default_config, clients=clients, projects=projects, helper=helper)


    def clicked_menu_project_checker(self):
        self.dialog = ProjectCheckerDialog(project_checker_dialog, default_config)

    
    def clicked_menu_project_upload(self):
        self.dialog = ProjectUploadDialog(project_upload_dialog, default_config)


    def clicked_submenu_settings(self):
        self.dialog = SettingsDialog(settings_dialog, default_config)


    def clicked_pb_deliver(self):
        client = self.client_list.currentItem().text()
        project = self.project_tree.currentItem().parent().text(0)
        job = self.project_tree.currentItem().text(0)

        deliver_loc = io.Manager(self.project_root).dir_from_root(
            client, project, job, 'Deliverables'
        )
        io.OsOpen(deliver_loc).open()


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
    default_config = Config()

    if default_config.project_drive:
        app = QApplication(sys.argv)
        # app.setQuitOnLastWindowClosed(False)
        main = MainWindow(main_res, default_config)

        # Create the icon
        icon = QIcon(heart_artwork)

        # Create the tray
        tray = QSystemTrayIcon()
        tray.setIcon(icon)
        tray.setVisible(True)

        menu = QMenu()
        exit_action = QAction("Exit")
        exit_action.triggered.connect(app.instance().quit)

        menu.addAction(exit_action)

        tray.setContextMenu(menu)

        sys.exit(app.exec_())

    else:
        print('Error Starting application.')
