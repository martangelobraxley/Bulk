import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QFileDialog, QListWidget, QVBoxLayout, QPushButton, QWidget, QDockWidget, QTextEdit
from PyQt5.QtCore import Qt
from editor import DocumentEditor
from file_manager import FileManager
from change_tracker import ChangeTracker

class BulkDocumentEditorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Bulk Document Editor")
        self.setGeometry(100, 100, 1200, 800)

        # Initialize core components
        self.change_tracker = ChangeTracker()
        self.editor = DocumentEditor(self.change_tracker)
        self.file_manager = FileManager()

        # Connect the change_tracked signal to a method to update the log
        self.editor.change_tracked.connect(self.update_activity_log)

        # Set up UI layout
        self.init_ui()

    def init_ui(self):
        # Main layout with tabs for multiple documents
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tabs.addTab(self.editor.get_editor_widget(), "Editor")

        # Add toolbar to the main window
        self.addToolBar(Qt.TopToolBarArea, self.editor.get_toolbar())

        # Side panel for managing file list and changes
        self.file_list = QListWidget()
        self.file_list.itemClicked.connect(self.on_file_selected)

        load_ref_btn = QPushButton("Load Reference Document")
        load_ref_btn.clicked.connect(self.load_reference_document)

        load_btn = QPushButton("Load Document")
        load_btn.clicked.connect(self.load_document)

        apply_changes_btn = QPushButton("Apply Changes")
        apply_changes_btn.clicked.connect(self.apply_changes)

        side_layout = QVBoxLayout()
        side_layout.addWidget(load_ref_btn)
        side_layout.addWidget(self.file_list)
        side_layout.addWidget(load_btn)
        side_layout.addWidget(apply_changes_btn)

        side_panel = QDockWidget("File Manager", self)
        side_widget = QWidget()
        side_widget.setLayout(side_layout)
        side_panel.setWidget(side_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, side_panel)

        self.activity_log = QTextEdit()
        self.activity_log.setReadOnly(True)
        log_panel = QDockWidget("Activity Log", self)
        log_panel.setWidget(self.activity_log)
        self.addDockWidget(Qt.RightDockWidgetArea, log_panel)

    def load_reference_document(self):
        file_dialog = QFileDialog()
        doc_path, _ = file_dialog.getOpenFileName(self, "Open Reference Document", "", "Word Documents (*.docx)")
        if doc_path:
            self.editor.load_document(doc_path)
            self.change_tracker.clear_changes()
            self.activity_log.append(f"Loaded reference document: {doc_path}")

    def load_document(self):
        file_dialog = QFileDialog()
        doc_path, _ = file_dialog.getOpenFileName(self, "Open Document", "", "Word Documents (*.docx)")
        if doc_path:
            self.file_manager.add_file(doc_path)
            self.file_list.addItem(doc_path)

    def on_file_selected(self, item):
        self.editor.load_document(item.text())

    def apply_changes(self):
        selected_files = [item.text() for item in self.file_list.selectedItems()]
        self.change_tracker.apply_changes(selected_files)
        self.activity_log.append(f"Applied changes to {len(selected_files)} document(s)")

    def update_activity_log(self, change_message):
        self.activity_log.append(change_message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BulkDocumentEditorApp()
    window.show()
    sys.exit(app.exec_())
