
import json

class ChangeTracker:
    def __init__(self):
        self.changes = []

    def track_change(self, change_type, text, context_before, context_after):
        # Log change details
        change_log = {
            "type": change_type,
            "text": text,
            "context_before": context_before,
            "context_after": context_after
        }
        self.changes.append(change_log)

    def apply_changes(self, file_list):
        # This should iterate over the selected files and apply tracked changes
        for file_path in file_list:
            self.apply_changes_to_document(file_path)

    def apply_changes_to_document(self, file_path):
        # Logic for applying changes to each document
        pass  # Extend this method with actual change application logic

    def export_log(self, path):
        # Export changes log as a JSON or Word file
        with open(path, 'w') as log_file:
            json.dump(self.changes, log_file, indent=4)

    def clear_changes(self):
        self.changes = []  # Clears the change log for a new reference document
