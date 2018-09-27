import sys
 
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton, QLineEdit, QListWidget, QTreeWidget, QTreeWidgetItem
from PySide2.QtCore import QFile, QObject

from modules import folder
 

# TODO: imp getting of issued information
# using TreeList as temp right now.
TreeList = ({

    'Header1': ((
        'Item11',
        'Item12',
    )),

    'Header2': ((
        'Item21',
        'Item22'
    ))
})


class Form(QObject):
    def __init__(self, ui_file, parent=None):
        super(Form, self).__init__(parent)
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)
 
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()

        # elements
        self.client_list = self.window.findChild(QListWidget, 'client_list')
        self.project_list = self.window.findChild(QListWidget, 'project_list')
        self.issued_tree = self.window.findChild(QTreeWidget, 'issued_tree')

        # wiring
        self.client_list.itemSelectionChanged.connect(self.client_list_changed)
        self.project_list.itemSelectionChanged.connect(self.project_list_changed)

        self.issued_tree.expandAll()

        clients = folder.ProjectMan('z:\\').walk_clients()
        
        for client in clients:
            self.client_list.addItem(client)
        
        self.window.show()


    def get_project_list(self, client_name):
        return folder.ProjectMan('z:\\').walk_project(client_name)


    def client_list_changed(self):
        client_name = self.client_list.currentItem().text()
        return self.update_project_list(client_name)


    def project_list_changed(self):
        client_name = self.client_list.currentItem().text()
        project_name = self.project_list.currentItem().text()
        self.issued_tree.clear()

        for key, value in TreeList.items():
            root = QTreeWidgetItem(self.issued_tree, [key])

            for val in value:
                item = QTreeWidgetItem([val])
                root.addChild(item)


    def update_project_list(self, client_name):
        t = folder.ProjectMan('z:\\').walk_client_projects(client_name)
        self.project_list.clear()
        for project in t:
            self.project_list.addItem(project)

        return t
 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form('main.ui')
    sys.exit(app.exec_())