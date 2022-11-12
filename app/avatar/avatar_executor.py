from app.executor import Executor
from app.avatar.avatar_context import AvatarContext

# Got 17 keypoint, make their average visibility 0.8
VISIBILITY_BENCHMARK = 17 * 0.8


class AvatarDefaultExecutor(Executor):
    def __init__(self):
        super(AvatarDefaultExecutor, self).__init__()
        print("init avatar default executor")
        self.context = AvatarContext()

    def execute(self, results):
        super(AvatarDefaultExecutor, self).execute(results)
        print('do the job')
        self.analyze_results(results)

    def analyze_results(self, results):
        actual_results = results['results']
        labels = results['labels']
        threshold = results['threshold']
        if 'boxes' in actual_results and len(actual_results['boxes']) > 0:
            self.find_person_and_say_hello(actual_results['boxes'], labels, threshold)
        if 'keypoint' in actual_results and len(actual_results['keypoint']) > 0:
            self.find_person_action(actual_results)

    def find_person_action(self, results):
        keypoint = results['keypoint']
        count = len(keypoint)
        print(f'got {count} persons')
        print('===== interact according action')
        visible_person = 0
        for points in keypoint:
            visibility = 0
            for point in points:
                visibility = visibility + point[2]
            if visibility > VISIBILITY_BENCHMARK:
                print(visibility)
                visible_person = visible_person + 1
        if visible_person > 0:
            self.context.frame_come(1)
        else:
            self.context.frame_come(0)
        print(f'got {visible_person} visible persons')

    def find_person_and_say_hello(self, boxes, labels, threshold):
        count = 0
        for box in boxes:
            clsid, bbox, score = int(box[0]), box[2:], box[1]
            name = labels[clsid]
            if name == 'person' and score > threshold:
                count += 1
        print(f'got {count} persons')


class AvatarKeypointExecutor(Executor):
    def __init__(self):
        super(AvatarKeypointExecutor, self).__init__()
        print("init avatar keypoint handler")

    def execute(self, results):
        super(AvatarKeypointExecutor, self).execute(results)
        print('do the keypoint job')