from main import RequestTask, TaskNode
from typing import Set

test_tasks = [
    {
        "name":"Mix the dry ingredients",
        "time":"2",
        "parallelizable":"false",
        "depends":[]
    },

    {
        "name":"Allow the butter and egg to reach room temperature",
        "time":"10",
        "parallelizable":"true",
        "depends":[]},
    {
        "name":"Mix the butter, sugar, egg, and vanilla in a bowl",
        "time":"3",
        "parallelizable":"false",
        "depends":["Allow the butter and egg to reach room temperature"]
    },
    {
        "name":"Combine the try and wet ingredients",
        "time":"5",
        "parallelizable":"false",
        "depends":["Mix the dry ingredients", "Mix the butter, sugar, egg, and vanilla in a bowl"]
    },
    {
        "name":"Add the chocolate chips",
        "time":"1",
        "parallelizable":"false",
        "depends":["Combine the try and wet ingredients"]
    },
    {
        "name":"Chill the dough",
        "time":"60",
        "parallelizable":"true",
        "depends":["Add the chocolate chips"]
    },
    {
        "name":"Roll the dough into balls",
        "time":"10",
        "parallelizable":"false",
        "depends":["Chill the dough"]
    },
    {
        "name":"Preheat the oven",
        "time":"15",
        "parallelizable":"true",
        "depends":[]
    },
    {
        "name":"Bake the cookies",
        "time":"15",
        "parallelizable":"true",
        "depends":["Roll the dough into balls", "Preheat the oven"]
    }
]

test_results = {
    'Mix the dry ingredients': 0, 
    'Allow the butter and egg to reach room temperature': 0, 
    'Mix the butter, sugar, egg, and vanilla in a bowl': 10, 
    'Preheat the oven': 0, 
    'Combine the try and wet ingredients': 13, 
    'Add the chocolate chips': 18, 
    'Chill the dough': 19, 
    'Roll the dough into balls': 79,
    'Bake the cookies': 89
}

if __name__ == "__main__":
    
    for i in range(len(test_tasks)):
        test_tasks[i] = RequestTask(**test_tasks[i]) #type: ignore

    #for task in tasks:
    #    print(task)

    task_tree = TaskNode.calculate_times([TaskNode.from_request_task(task) for task in test_tasks]) #type: ignore
    print()
    print()
    print()
    assert task_tree == test_results, "The correct solution is not provided!"
    for task in task_tree.items():
        print(task)
