
from Queue import Queue
from threading import Thread, RLock
import logging

log = logging.getLogger(__name__)


DOWNLOAD = 1
EXIT = 2

class MPStreamer(object):
    
    INF_UNKNOWN_CMD = "Unknown command received: %s"
    DBG_EXIT_CMD = "Received command exit!"
    
    _id_lock = RLock()
    _current_id = 0
    
    @classmethod
    def nextId(cls):
        
        _id_lock.acquire()
        try:
            id = _id_lock
            _id_lock += 1
            return id
        finally:
            _id_lock.release()
    
    def __init__(self, dl_path, mp_path='mplayer', name="worker"):
        self._dl = dl_path
        self._mplayer = mp_path
        self._queue = Queue.Queue
        self._name = "%s_%02d" % (name, self.nextId())
        self._thread = Thread(target=self._workerloop)
        self._log = log
    
    def _workerloop(self):
        
        running = True
        while running:
            cmd = self._queue.get(True)
            if cmd[0] == DOWNLOAD:
                pass
            elif cmd[1] == EXIT:
                log.debug(
                return
            else:
                log.info(self.INF_UNKNOWN_CMD % str(cmd[0]))
                
