from redis import Redis
from schema.task import TaskSchema
import json 

class TaskCache:
    def __init__(self, redis: Redis):
        self.redis = redis 

    def get_tasks(self) -> list[TaskSchema]:
        with self.redis as redis:
            tasks_json = redis.lrange("tasks", 0, -1)
            return [TaskSchema.model_validate(json.loads(task)) for task in tasks_json]

    def set_tasks(self, tasks: list[TaskSchema]):
        if not tasks:
            self.redis.delete("tasks")
            return
        tasks_json = [task.model_dump_json() for task in tasks]
        with self.redis as redis:
            redis.delete("tasks")
            redis.lpush("tasks", *tasks_json)

