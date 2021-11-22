import datetime
from threading import Timer


class FolderWatcher:

    def __init__(self):
        self.period = None
        self.t = None

    def start(self, folder: str, period: datetime.timedelta = datetime.timedelta(seconds=10)):
        print(f'START for {period.seconds} sec, or {period.seconds / 60} min')
        self.period = period
        self._start()

    def _start(self):
        self.t = Timer(self.period.seconds, self.process)
        self.t.start()

    def stop(self):
        print('STOP')
        self.t.stop()

    def process(self):
        print('   process')
        self._start()
