from PyQt5.QtWidgets import QListWidgetItem

class FileManager:
    def __init__(self):
        self.files = []

    def add_file(self, path):
        item = QListWidgetItem(path)
        self.files.append(item)
        return item  # To add to QListWidget in main UI

    def get_files(self):
        return self.files
