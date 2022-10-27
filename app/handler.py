import asyncio
import os
import yaml

from app.avatar.avatar_executor import AvatarDefaultExecutor
from app.avatar.avatar_executor import AvatarKeypointExecutor


async def handle(app_name, infer_name, results):
    print(f'handle results {app_name}')
    print(f'infer name {infer_name}')
    config_file = os.path.join('app', app_name, 'configs/executor_cfg.yml')
    with open(config_file) as f:
        executor_conf = yaml.safe_load(f)
    executor_name = executor_conf[infer_name]['executor']
    executor = eval(executor_name)()
    executor.execute(results)


async def handle_task(app_name, infer_name, results):
    asyncio.create_task(handle(app_name, infer_name, results))
