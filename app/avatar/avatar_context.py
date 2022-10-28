import yaml
import socket


class AvatarContext(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AvatarContext, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        with open('app/avatar/configs/executor_cfg.yml') as f:
            self.executor_conf = yaml.safe_load(f)
        self.udp_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
