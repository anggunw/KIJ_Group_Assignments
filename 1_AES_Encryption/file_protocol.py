import json
import logging

from file_interface import FileInterface


class FileProtocol:
    def __init__(self):
        self.file = FileInterface()

    def process_string(self, string_input=''):
        logging.warning(f"process string: {string_input}")
        c = string_input.split(" ")
        try:
            c_request = c[0].strip()
            logging.warning(f"processing request: {c_request}")
            if c_request == 'send':
                filename = c[1].strip()
                filedata = ""
                for w in c[2:]:
                    filedata = "{}{}".format(filedata, w)
                print(f"filedata: {filedata}")
                return json.dumps(self.file.send(filename, filedata))
            if c_request == 'get':
                filename = c[1].strip()
                return json.dumps(self.file.get(filename))
            else:
                return json.dumps(dict(status='ERROR', message='unknown request'))
        except Exception as e:
            return json.dumps(dict(status='ERROR', message=str(e)))
