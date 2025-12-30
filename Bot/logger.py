from datetime import datetime


class Logger:

    def __init__(self, logfilepath: str = '.'):
        self.logfilepath = logfilepath

    def log(self, write_type: str, utgid: int, userid: int, add_text: str = ''):
        with open(self.logfilepath, 'a') as f:
            f.write(
                f'[{datetime.now().strftime('%d/%m/%Y|%H:%M:%S')}] [DB_id:{userid} TG_id:{utgid}] [{write_type}] info:[{add_text}]'
            )

