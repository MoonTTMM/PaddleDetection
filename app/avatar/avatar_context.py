import yaml
import socket
from queue import Queue
from threading import Timer

QUEUE_MAXSIZE = 6
PERSON_IN_COUNT = 0
PERSON_OUT_COUNT = 0


# info from frame sequence would be record here.
class AvatarContext(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AvatarContext, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        with open('app/avatar/configs/executor_cfg.yml') as f:
            self.executor_conf = yaml.safe_load(f)
        self.udp_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.frame_queue = Queue(QUEUE_MAXSIZE)
        self.person_exist = False
        self.person_in = False
        # cooling time for the greeting
        self.person_timer = Timer(30, lambda: print('timer end'))

    def frame_come(self, person):
        if self.frame_queue.qsize() == QUEUE_MAXSIZE:
            self.frame_queue.get()
        self.frame_queue.put(person)
        count = 0
        for i in range(self.frame_queue.qsize()):
            count = count + self.frame_queue.queue[i]
        if count >= PERSON_IN_COUNT:
            if self.person_exist is False:
                self.person_appear()
            self.person_exist = True
        elif count <= PERSON_OUT_COUNT:
            if self.person_exist is True:
                self.person_leave()
            self.person_exist = False

    def person_appear(self):
        if self.person_timer.is_alive():
            return
        self.person_timer = Timer(30, lambda: print('timer end'))
        self.person_timer.start()
        self.greeting()
        print('we got visitor here')

    def person_leave(self):
        print('our visitor leaves')

    def greeting(self):
        ip = self.executor_conf['controller_ip']
        port = self.executor_conf['controller_port']
        print('act to avatar')
        content = 'SayHello'.encode('utf-8')
        self.udp_client_socket.sendto(content, (ip, port))