from app.executor import Executor


class AvatarDefaultExecutor(Executor):
    def __init__(self):
        super(AvatarDefaultExecutor, self).__init__()
        print("init avatar default executor")

    def execute(self, results):
        super(AvatarDefaultExecutor, self).execute(results)
        print('do the default job')


class AvatarKeypointExecutor(Executor):
    def __init__(self):
        super(AvatarKeypointExecutor, self).__init__()
        print("init avatar keypoint handler")

    def execute(self, results):
        super(AvatarKeypointExecutor, self).execute(results)
        print('do the keypoint job')