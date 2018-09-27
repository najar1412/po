import sys
 
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton, QLineEdit, QListWidget, QTreeWidget, QTreeWidgetItem
from PySide2.QtCore import QFile, QObject

from modules import folder
 

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
        self.project_root = 'z:\\'
        self.project_name = ''

        # widgets
        self.client_list = self.window.findChild(QListWidget, 'client_list')
        self.project_tree = self.window.findChild(QTreeWidget, 'project_tree')
        self.issued_tree = self.window.findChild(QTreeWidget, 'issued_tree')

        # widget actions
        self.client_list.itemSelectionChanged.connect(self.action_client_list_changed)
        self.project_tree.itemSelectionChanged.connect(self.action_project_tree_changed)

        # start up logic
        self.get_clients()
        self.window.show()


    def get_clients(self):
        """appends list of clients to client_list"""
        clients = folder.ProjectMan(self.project_root).walk_clients()
        
        for client in clients:
            self.client_list.addItem(client)


    def action_client_list_changed(self):
        """logic to run when user selects a Client"""
        self.project_tree.clear()
        client_name = self.client_list.currentItem().text()

        return self.update_project_tree(client_name)


    def action_project_tree_changed(self):
        """logic to run when user selects a project/job"""
        client_name = self.client_list.currentItem().text()
        t = folder.ProjectMan(self.project_root).walk_client_projects(client_name)

        getSelection = self.project_tree.selectedItems()
        if getSelection:
            baseNode = getSelection[0]
            get_child_node = baseNode.text(0)

            if get_child_node not in t:
                self.update_issued_tree(get_child_node)

                return get_child_node
            else:
                self.project_name = get_child_node

        return False


    def update_project_tree(self, client_name):
        """updates the project tree, when a new client is selected"""
        self.project_tree.clear()
        self.issued_tree.clear()

        t = folder.ProjectMan(self.project_root).walk_client_projects(client_name)

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
        t = folder.ProjectMan(self.project_root).walk_client_project_issued(client_name, self.project_name, job)

        for key, value in t.items():
            root = QTreeWidgetItem(self.issued_tree, [key])

            if len(value) > 0:
                for val in value:
                    item = QTreeWidgetItem([val])
                    root.addChild(item)

        return True
 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form('main.ui')
    sys.exit(app.exec_())