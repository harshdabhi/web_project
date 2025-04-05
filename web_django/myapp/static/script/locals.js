document.addEventListener("DOMContentLoaded", function () {
    const addMachineForm = document.getElementById("add-machine-form");
    const removeMachineForm = document.getElementById("remove-machine-form");
    const machineTableBody = document.querySelector("#all-machines tbody");

    function getMachines() {
        return JSON.parse(localStorage.getItem("machines")) || [];
    }

    function saveMachines(machines) {
        localStorage.setItem("machines", JSON.stringify(machines));
    }

    function displayMachines() {
        machineTableBody.innerHTML = "";
        const machines = getMachines();
        machines.forEach(machine => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${machine.name}</td>
                <td>OK</td>
                <td>${machine.location}</td>
                <td><button class="btn remove-btn" data-name="${machine.name}">Remove</button></td>
            `;
            machineTableBody.appendChild(row);
        });
    }

    addMachineForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const name = document.getElementById("machine-name").value.trim();
        const location = document.getElementById("machine-location").value.trim();
        if (name && location) {
            const machines = getMachines();
            machines.push({ name, location });
            saveMachines(machines);
            displayMachines();
            addMachineForm.reset();
        }
    });

    removeMachineForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const name = document.getElementById("remove-machine-name").value.trim();
        let machines = getMachines();
        machines = machines.filter(machine => machine.name !== name);
        saveMachines(machines);
        displayMachines();
        removeMachineForm.reset();
    });

    machineTableBody.addEventListener("click", function (e) {
        if (e.target.classList.contains("remove-btn")) {
            const name = e.target.getAttribute("data-name");
            let machines = getMachines();
            machines = machines.filter(machine => machine.name !== name);
            saveMachines(machines);
            displayMachines();
        }
    });

    displayMachines();
});
