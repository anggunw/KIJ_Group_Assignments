import base64


class FileInterface:
    def send(self, filename='', filedata=''):
        try:
            filedata = base64.b64decode(filedata)
            fp = open(filename, 'wb+')
            fp.write(filedata)
            fp.close()
            return dict(status='OK')
        except Exception as e:
            return dict(status='ERROR', message=str(e))

    def get(self, filename=''):
        if filename == '':
            return None
        try:
            fp = open(f"{filename}", 'rb')
            filedata = base64.b64encode(fp.read()).decode()
            print(filedata)
            return dict(status='OK', filename_data=filename, file_data=filedata)
        except Exception as e:
            return dict(status='ERROR', message=str(e))
