from app.executor import Executor
from app.avatar.avatar_context import AvatarContext


class AvatarDefaultExecutor(Executor):
    def __init__(self):
        super(AvatarDefaultExecutor, self).__init__()
        print("init avatar default executor")
        self.context = AvatarContext()

    def execute(self, results):
        super(AvatarDefaultExecutor, self).execute(results)
        print('do the default job')
        actual_results = results['results']
        labels = results['labels']
        threshold = results['threshold']

        if 'boxes' in actual_results and len(actual_results['boxes']) > 0:
            self.find_person_and_say_hello(actual_results['boxes'], labels, threshold)
        if 'keypoint' in actual_results and len(actual_results['keypoint']) > 0:
            self.find_person_action(actual_results)

    def find_person_action(self, results):
        print('===== interact according action')

    def find_person_and_say_hello(self, boxes, labels, threshold):
        udp_client = self.context.udp_client_socket
        ip = self.context.executor_conf['controller_ip']
        port = self.context.executor_conf['controller_port']
        count = 0
        for box in boxes:
            clsid, bbox, score = int(box[0]), box[2:], box[1]
            name = labels[clsid]
            if name == 'person' and score > threshold:
                count += 1
                content = 'SayHello'.encode('utf-8')
                udp_client.sendto(content, (ip, port))
        print(f'got {count} persons')


class AvatarKeypointExecutor(Executor):
    def __init__(self):
        super(AvatarKeypointExecutor, self).__init__()
        print("init avatar keypoint handler")

    def execute(self, results):
        super(AvatarKeypointExecutor, self).execute(results)
        print('do the keypoint job')