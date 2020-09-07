from remarkable.uploader import Uploader

FILE_TO_UPLOAD = ""

if __name__ == '__main__':
    uploader = Uploader()
    uploader.upload_file_to_folder(FILE_TO_UPLOAD, "Economist")
