
"""Author: Saygın Efe Yıldız"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, RootModel, field_validator, ValidationError
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
    depends: Set[str]

class RequestTaskList(RootModel[RequestTask]):
    root: List[RequestTask]

    @field_validator('root')
    @classmethod
    def all_names_must_be_unique(cls, root: List[RequestTask]):
        request_names = [request_task.name for request_task in root]
    
        if len(request_names) != len(set(request_names)):
            raise ValueError("The tasks are not unique")
        return root

class TaskNode:
    def __init__(self, name: str, time: int, parallelizable: bool, depends: Set[str]):
        self.name: str = name
        self.time: int = time
        self.init_time: int = time
        self.parallelizable: bool = parallelizable
        self.depends: Set[str] = depends

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.name

class TaskNodeTree:
    def __init__(self, request_task_list: RequestTaskList):
        self.tasks: List[TaskNode] = self.__from_request_task_list(request_task_list)
        #TODO: Validate the tasks are in fact valid and that there are no duplicated and that etc.

    def __from_request_task_list(self, request_task_list: RequestTaskList) -> List[TaskNode]:
        return [TaskNode(**dict(request_task)) for request_task in request_task_list.root]

    def calculate_times(self) -> Dict[str, int]:
        time = 0
        dtime = 0
        calculated_dict = {}
        #Get leaf nodes
        working_list = [task for task in self.tasks if task.depends == set()]
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

            if shortest_task in self.tasks:
                self.tasks.remove(shortest_task)

            dtime = shortest_task.time
            time += dtime
            calculated_dict[shortest_task.name] = time - shortest_task.init_time

            for pt in parallelizable_tasks:
                pt.time -= dtime
            if shortest_task.parallelizable and len(not_parallelizable_tasks) > 0:
                not_parallelizable_tasks[0].time -= dtime
            
            for task in self.tasks:
                print(f"Task:  {task}")
                print(f"Calculated:            {set(calculated_dict.keys())}")
                print(f"Dependencies of task:  {task.depends}")
                if task.depends != set() and task.depends.issubset(set(calculated_dict.keys())):

                    working_list.append(task)
                    print(f"Appended: {task}")
        return calculated_dict
        
@app.post("/")
async def root(tasks: RequestTaskList) -> Dict[str, int]:
    task_tree: TaskNodeTree = TaskNodeTree(tasks)
    calculated_times = task_tree.calculate_times()
    print(tasks)
    print(task_tree)
    return calculated_times
