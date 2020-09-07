from pathlib import Path
from rmapy.api import Client
from rmapy.document import ZipDocument
from rmapy.folder import Folder

rmapy = Client()
rmapy.renew_token()


class Uploader:
    def __init__(self):
        self._rmapy = Client()
        self._rmapy.renew_token()

    def upload_file_to_folder(self, file: str, folder_name: str):
        folder = self._find_folder(folder_name)
        document = ZipDocument(doc=file)
        document.metadata["VissibleName"] = Path(file).stem
        self._rmapy.upload(document, folder)

    def _find_folder(self, folder_name: str) -> Folder:
        return next(item for item in self._rmapy.get_meta_items() if
                    isinstance(item, Folder) and item.VissibleName == folder_name)
