
# Cookie Homework

## Problem Definition

Cookie Homework is the voluntary assignment given by [Bora Canbula](https://github.com/canbula) for the [Parallel Programming course](https://github.com/syildizz/ParallelProgrammingCBU) in the Fall Semestre of 2023-2024. 
To demonstrate the cookie homework, [Bora Canbula](https://github.com/canbula) built the website [Cookie Baker](https://canbula.com/cookie) as a part of the [course](https://github.com/syildizz/ParallelProgrammingCBU/tree/master/Week04/cookie-baker).

The [Cookie Baker](https://canbula.com/cookie) website is a simple simulation of a cookie baking recipe which is used as a demonstration for parallel programming. 
Just like tasks and processes, 
some of the steps in the recipe are parallelizable whilst others are not. 
Some of the steps in the recipe depend on others and some do not. 
The steps take different length of time to complete. 
The [Cookie Baker](https://canbula.com/cookie) website calculates the final time of the baking stage after all of the tasks are done.

In The Cookie Homework assignment the goal is to order the baking recipe steps so that the minimum amount of time is taken to complete the baking process. 
The code in this repository solves for the order of tasks that which minimizes the baking time. 
The Cookie Homework project not only provides a solution the original problem but it also solves any problem that is similar in concept.

## Project Structure

The Cookie Homework assignment was gives with the requirement of using a server-client architecture as a challenge. 
The project consists of a backend and a frontend code which communicate with each other using JSON.

The frontend is developed using [vanilla javascript](http://vanilla-js.com/) without any dependencies.

The backend is developed using Python. 
For the backend REST api, the [FastAPI](https://fastapi.tiangolo.com/) module is used.
For JSON parsing and input validation, the [Pydantic](https://docs.pydantic.dev/latest/) module is used.

## Methodology

The frontend sends a JSON query to the backend, made up of a list of tasks 
which differ in terms of 
 - Length of time to complete the task 
 - Parallelizability of the task
 - The dependencies of the tasks between each other

### Data input

The tasks are stored in a global array in the frontend. 
When sending to the backend, the array object is serialized into a JSON string 
and then send.

The backend receives the JSON query using FastAPI. 
When the JSON is received, it is validated and deserialized into a Python object using Pydantic.

### Calculating times

The tasks are simulated to run by using a simulated clock. Each time a task is removed, the time that the task takes to complete is added to the clock. 
If there are parallelizable tasks which do not have dependencies, that amount of passed time is subtracted from their remining time. This is because parallel tasks which do not have dependencies run simultaneously with the removed task.

The tasks without any dependencies are first chosen and sorted by length in ascending order.
As tasks are removed, the tasks that depend on the removed tasks become available. The process is repeated until all the tasks are completed. 

When a task is removed, the time at which it is removed is stored. This allows us to track when each task ends. This gives us a list of tasks ordered to minimize the total time taken to complete all the tasks.

### Data output

The backend serializes the task list into JSON and sends it back to the frontend. The frontend displays the calculated result.

## Deployment

The project dependencies are listed in the [requirements.txt](requirements.txt) file. 

The [run.sh](run.sh) file can be used to start the web server. It uses [Uvicorn](https://www.uvicorn.org/) as the ASGI web server.
