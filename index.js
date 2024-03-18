//Author: Saygın Efe Yıldız

class Task {

    static htmlForm;
    static tasks = [];

    constructor(name, time, parallelizable, depends) {
        this.name = name;
        this.time = time;
        this.parallelizable = parallelizable;
        this.depends = depends;
        this.element;
    }

    createElement() {
        let htmlArticle = document.createElement("article");
        htmlArticle.classList.add("task-article");
        let htmlString = `
            <article class="task-article">
            <div class="task-name">${this.name}</div>
            <div class="task-time">${this.time}</div>
            <div class="task-parallelizable">${(this.parallelizable) ? "Is parallelizable" : "Not parallelizable"}</div>
        `;
        if (this.depends.length !== undefined && this.depends.length > 0) {
            let dependString = ""
            for (let depend of this.depends) {
                dependString += `${depend}, `
            }
            htmlString += `<div class="task-depends">Depends on ${dependString}</div>`
        }
        htmlString += `
            <button>Delete</button>
            </article>
        `

        htmlArticle.innerHTML = htmlString;

        htmlArticle.getElementsByTagName('button')[0].addEventListener("click", (e) => {
            this.destructor();
        });

        this.element = htmlArticle;

        return htmlArticle;
    }

    destructor() {
        this.element.remove();
        const index = Task.tasks.indexOf(this);

        if (index > -1) {
            Task.tasks.splice(index, 1);
        } else {
            console.log("Index was smaller than -1");
        }
        this.deleteDependingTasks();
        Task.updateTaskNames();
    }

    static async sendTasksToServer(elem) {
        try {
            const response = await fetch("http://127.0.0.1:8000/", {
                method: "POST", // or 'PUT'
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(Task.tasks, ["name", "time", "parallelizable", "depends"]),
            });

            const result = await response.json();
            console.log("Success:", result);
            let elemString = "";
            for (const [key, value] of Object.entries(result)) {
                console.log(key, value);
                elemString += `Task ${key} starts at ${value} time`;
                elemString += "<br />";
            }
            elem.innerHTML = elemString;
        } catch (error) {
            console.error("Error:", error);
            elem.textContent = error;
        }
    }

    static updateTaskNames() {
        let htmlDependsInput = this.htmlForm.querySelector("#task_depends")
        //let currentTaskNames = document.getElementsByClassName("task-name");
        let currentTaskNames = Task.tasks.map(t => t.name);

        let optionsString = `
            <option value="None">None</option>
        `;
        for (let taskName of currentTaskNames) {
            console.log(taskName);
            optionsString += `<option value=${taskName.replace(/ /g, "_")}>${taskName}</option>`;
        }
        htmlDependsInput.innerHTML = optionsString;
    }

    deleteDependingTasks() {
        const found = Task.tasks.filter(t => t.depends.includes(this.name));
        for (let f of found) {
            f.destructor();
        }
    }

    static createTaskForm() {

        let taskFormString = `
            <label for="task_name">Name of your task</label>
            <input type="text" id="task_name" name="name" placeholder="Bake Cookies">
            <label for="task_time">Time it takes for your task to be complete </label>
            <input type="number" id="task_time" name="time" placeholder="10">
            <label for="task_parallelizable">Is this task parallelizable?</label>
            <input type="checkbox" id="task_parallelizable" name="parallelizable">
            <label for="task_depends">What does this task depend on?</label>
            <select id="task_depends" name="depends" multiple>
            <input type="submit" id="task_submit" name="submit" value="Add to tasks">
        `
        this.htmlForm = document.createElement("form");
        this.htmlForm.classList.add("task-form")
        this.htmlForm.innerHTML = taskFormString;
        this.updateTaskNames();

        this.htmlForm.addEventListener("submit", (e) => {
            e.preventDefault(); 
            console.log(Array.from(this.htmlForm.elements["depends"].options)
                .map(o => o.selected ? o.textContent : "None")
                .filter(o => o !== "None")
            );
            let newTask = new Task(this.htmlForm.elements["name"].value, 
                this.htmlForm.elements["time"].value, 
                this.htmlForm.elements["parallelizable"].checked,
                Array.from(this.htmlForm.elements["depends"].options)
                    .map(o => o.selected ? o.textContent : "None")
                    .filter(o => o !== "None")
            );
            this.tasks.push(newTask);
            this.htmlForm.parentNode.insertBefore(newTask.createElement(), this.htmlForm);
            this.htmlForm.elements["name"].value = "";
            this.htmlForm.elements["time"].value = "";
            this.htmlForm.elements["parallelizable"].checked = false;
            this.updateTaskNames();
        });

        return this.htmlForm;
    }

    static generateTasksFromArray(taskObject) {
        this.htmlForm.elements["name"].value = taskObject.name;
        this.htmlForm.elements["time"].value = taskObject.time;
        this.htmlForm.elements["parallelizable"].checked = taskObject.parallelizable;
        let select_element = this.htmlForm.elements["depends"];
        let optionsToSelect = taskObject.options
        for (var i = 0, l = select_element.options.length, o; i < l; i++) {
            o = select_element.options[i];
            if (optionsToSelect.indexOf(o.text) != -1) {
                o.selected = true;
            }
        }
        this.htmlForm.elements["submit"].click()
        //cleanup
        this.htmlForm.elements["name"].value = "";
        this.htmlForm.elements["time"].value = "";
        this.htmlForm.elements["parallelizable"].checked = false;
    }

}



let taskSection = document.getElementById("task_section");
if (taskSection == null) {
    console.log("taskSection null");
}

let taskForm = Task.createTaskForm();
taskSection.appendChild(taskForm);

responseDiv = document.getElementById("server_response");

submitServerButton = document.createElement("button");
submitServerButton.id = "submit_server_button"
submitServerButton.textContent = "Submit to server"
taskSection.appendChild(submitServerButton);
submitServerButton.addEventListener("click", (e) => {
   Task.sendTasksToServer(responseDiv); 
});

TestDefaultButton = document.createElement("button");
TestDefaultButton.id = "test_default_button"
TestDefaultButton.textContent = "Initialize with default value"
taskSection.appendChild(TestDefaultButton);
TestDefaultButton.addEventListener("click", (e) => {
    tasks = [
                {
                    name: "Mix the dry ingredients",
                    time: 2,
                    parallelizable: false,
                    options: ["None"]
                },
                {
                    name: "Allow the butter and egg to reach room temperature",
                    time: 10,
                    parallelizable: true,
                    options: ["None"]
                },
                {
                    name: "Mix the butter, sugar, egg, and vanilla in a bowl",
                    time: 3,
                    parallelizable: false,
                    options: ["Allow the butter and egg to reach room temperature"]
                },
                {
                    name: "Combine the try and wet ingredients",
                    time: 5,
                    parallelizable: false,
                    options: ["Mix the dry ingredients", 
                              "Mix the butter, sugar, egg, and vanilla in a bowl"]
                },
                {
                    name: "Add the chocolate chips",
                    time: 1,
                    parallelizable: false,
                    options: ["Combine the try and wet ingredients"]
                },
                {
                    name: "Chill the dough",
                    time: 60,
                    parallelizable: true,
                    options: ["Add the chocolate chips"]
                },
                {
                    name: "Roll the dough into balls",
                    time: 10,
                    parallelizable: false,
                    options: ["Chill the dough"]
                },
                {
                    name: "Preheat the oven",
                    time: 15,
                    parallelizable: true,
                    options: ["None"]
                },
                {
                    name: "Bake the cookies",
                    time: 15,
                    parallelizable: true,
                    options: ["Roll the dough into balls",
                              "Preheat the oven"]
                }
            ]

    for (let task of tasks) {
        Task.generateTasksFromArray(task);
    }

});
