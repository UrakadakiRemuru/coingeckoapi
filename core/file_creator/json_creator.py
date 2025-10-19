import json

from core.file_creator import FileCreator


class JSONCreator(FileCreator):
    def create_file(self):
        with open(self.FILE_DIR / "data.json", "w", encoding='utf-8') as f:
            json.dump(self.obj, f, ensure_ascii=False, indent=4)
