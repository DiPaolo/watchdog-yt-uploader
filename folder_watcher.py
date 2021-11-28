import datetime
from threading import Timer


class FolderWatcher(object):
    def __init__(self):
        self.period = None
        self.t = None
        self.callback = None

    def start(self, callback, period: datetime.timedelta = datetime.timedelta(seconds=10)):
        print(f'START for {period.seconds} sec, or {period.seconds / 60} min')
        self.period = period
        self.callback = callback
        self._start()

    def _start(self):
        self.t = Timer(self.period.seconds, self.process)
        self.t.start()

    def stop(self):
        print('STOP')
        if self.t:
            self.t.cancel()
            self.t = None
        self.callback = None

    def is_running(self):
        return self.t is not None

    def process(self):
        print('   process')
        if self.callback:
            self.callback()
        self._start()
