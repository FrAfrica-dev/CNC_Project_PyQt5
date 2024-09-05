# file_handling.py
class FileHandler:
    def __init__(self):
        self.file_queue = []

    def add_file(self, file_name):
        """Adds a file to the queue for processing."""
        self.file_queue.append(file_name)
        print(f"Added {file_name} to the queue")

    def clear_queue(self):
        """Clears the queue of files."""
        self.file_queue = []
