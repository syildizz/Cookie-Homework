
"""Author: Saygın Efe Yıldız"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, RootModel
from typing import List, Set, Dict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequestTask(BaseModel):
    name: str
    time: int
    parallelizable: bool
    depends: List[str]

class RequestTaskList(RootModel[RequestTask]):
    root: List[RequestTask]

class TaskNode():
    def __init__(self, name: str, time: int, parallelizable: bool, depends_name: Set[str]):
        self.name = name
        self.time = time
        self.init_time = time
        self.parallelizable = parallelizable
        self.depends_name = depends_name

    @classmethod
    def from_request_task(cls, task: RequestTask):
        return cls(task.name, task.time, task.parallelizable, set(task.depends))

    @staticmethod
    def calculate_times(task_node_tree: List["TaskNode"]) -> Dict[str, int]:
        time = 0
        dtime = 0
        calculated_dict = {}
        #Get leaf nodes
        working_list = [task for task in task_node_tree if task.depends_name == set()]
        while working_list != []:
            working_list.sort(key=lambda t: t.time)

            not_parallelizable_tasks = [task for task in working_list if not task.parallelizable]
            not_parallelizable_tasks.sort(key=lambda t: t.time)
            parallelizable_tasks = [task for task in working_list if task.parallelizable]
            parallelizable_tasks.sort(key=lambda t: t.time)

            shortest_task = working_list.pop(0)
            print(f"Pulled: {shortest_task}")
            if shortest_task in working_list:
                working_list.remove(shortest_task)

            if shortest_task in task_node_tree:
                task_node_tree.remove(shortest_task)

            dtime = shortest_task.time
            time += dtime
            calculated_dict[shortest_task.name] = time - shortest_task.init_time

            for pt in parallelizable_tasks:
                pt.time -= dtime
            if shortest_task.parallelizable and len(not_parallelizable_tasks) > 0:
                not_parallelizable_tasks[0].time -= dtime
            
            for task in task_node_tree:
                print(f"Task:  {task}")
                print(f"Calculated:            {set(calculated_dict.keys())}")
                print(f"Dependencies of task:  {task.depends_name}")
                if task.depends_name != set() and task.depends_name.issubset(set(calculated_dict.keys())):
                    working_list.append(task)
                    print(f"Appended: {task}")
        return calculated_dict
        
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self):
        return self.name

@app.post("/")
async def root(tasks: RequestTaskList) -> Dict[str, int]:
    task_tree = TaskNode.calculate_times([TaskNode.from_request_task(task) for task in tasks.root])
    print(tasks)
    print(task_tree)
    return task_tree
