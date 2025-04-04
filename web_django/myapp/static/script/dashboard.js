export function GetAllMachines(tbody) {
  // clear the existing rows
  tbody.innerHTML = ""; // Clear existing rows

  fetch("/api/machines/", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${localStorage.getItem("auth_token")}`, // Use the token stored in localStorage
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to fetch machines");
      }
      return response.json();
    })
    .then((machines) => {
      if (machines == null || machines.length === 0) {
        const row = document.createElement("tr");
        row.innerHTML = `<td colspan="4">No machines available.</td>`;
        tbody.appendChild(row);
      } else {
        machines.forEach((machine) => {
          const row = document.createElement("tr");
          row.className = `machine-card ${machine.status.toLowerCase()}`;

          row.innerHTML = `
                                    <td>${machine.name}</td>
                                    <td>${machine.status}</td>
                                    <td>${machine.location}</td>
                                    <td><a href="/machine/${machine.id}" class="btn">View Details</a></td>
                                `;
          tbody.appendChild(row);
        });
      }
    })
    .catch((error) => {
      console.error("Error loading machines:", error);
      // display an error message to the user
      const row = document.createElement("tr");
      row.innerHTML = `<td colspan="5">Error loading fault cases. Please try again later.</td>`;
      tbody.appendChild(row);
    });
}

export function GetAllFaults(tbody) {
  // clear the existing rows
  tbody.innerHTML = ""; // Clear existing rows

  fetch("/api/faults/", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${localStorage.getItem("auth_token")}`, // Use the token stored in localStorage
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to fetch fault cases");
      }
      return response.json();
    })
    .then((cases) => {
      if (cases == null || cases.length === 0) {
        const row = document.createElement("tr");
        row.innerHTML = `<td colspan="5">No fault cases available.</td>`;
        tbody.appendChild(row);
      } else {
        cases.forEach((caseItem) => {
          const row = document.createElement("tr");
          row.className = `case-item ${caseItem.status.toLowerCase()}`;

          row.innerHTML = `
                                    <td>${caseItem.case_number}</td>
                                    <td>${caseItem.machine}</td>
                                    <td>${caseItem.created_at}</td>
                                    <td>${caseItem.status}</td>
                                    <td><a href="${caseItem.details_url}" class="btn">View Case</a></td>
                                `;
          tbody.appendChild(row);
        });
      }
    })
    .catch((error) => {
      console.error("Error loading fault cases:", error);
      // display an error message to the user
      const row = document.createElement("tr");
      row.innerHTML = `<td colspan="5">Error loading fault cases. Please try again later.</td>`;
      tbody.appendChild(row);
    });
}

export function GetAllWarnings(warningSection) {
  // clear the existing warnings
  warningSection.innerHTML = ""; // Clear existing warnings

  fetch("/api/warnings/", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${localStorage.getItem("auth_token")}`, // Use the token stored in localStorage
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to fetch machine warnings");
      }
      return response.json();
    })
    .then((warnings) => {
      if (warnings == null || warnings.length === 0) {
        const li = document.createElement("li");
        li.textContent = "No current warnings.";
        warningSection.appendChild(li);
      } else {
        warnings.forEach((warning) => {
          const li = document.createElement("li");
            // get the machine name from the machine ID

            // fetch the machine name from the server using the machine ID
            fetch("/api/machines/" + warning.machine + "/")
              .then((response) => response.json())
                .then((machine) => {
                    li.innerHTML = `<span>${machine.name}</span>: ${warning.text}`;
                    warningSection.appendChild(li);
                })
                .catch((error) => {
                    console.error("Error fetching machine name:", error);
                    // Fallback to using the machine ID if the name cannot be fetched
                    li.innerHTML = `<span>${warning.machine}</span>: ${warning.text}`;
                    warningSection.appendChild(li);
                }
            );
        });
      }
    })
    .catch((error) => {
      console.error("Error loading machine warnings:", error);
      // display an error message to the user
      const li = document.createElement("li");
      li.textContent =
        "Error loading machine warnings. Please try again later.";
      warningSection.appendChild(li);
    });
}

export function AddAllMachinesToSelect(machineSelect) {
  // Clear existing options
  machineSelect.innerHTML = '<option value="">-- Choose a Machine --</option>';

  // Fetch machines from the server
  fetch("/api/machines/")
    .then((response) => response.json())
    .then((data) => {
      data.forEach((machine) => {
        const option = document.createElement("option");
        option.value = machine.id;
        option.textContent = machine.name;
        machineSelect.appendChild(option);
      });
    })
    .catch((error) => console.error("Error fetching machines:", error));
}


export function updateAssignedMachines() {
    const tbody = document.querySelector("#assigned-machines tbody");

    const user_id = localStorage.getItem("user_id");
    const statusFilter = document.getElementById("status-filter").value;

    console.log("User ID:", user_id); // Log the user_id for debugging

    // clear the existing rows
    tbody.innerHTML = "";

    fetch(
      "/api/machines/assigned_to_user/?user_id=" +
        user_id +
        "&status=" +
        statusFilter,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${localStorage.getItem("auth_token")}`, // Use the token stored in localStorage
        },
      }
    )
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch assigned machines");
        }
        return response.json();
      })
      .then((machines) => {
        if (machines == null || machines.length === 0) {
          const row = document.createElement("tr");
          row.innerHTML = `<td colspan="4">No assigned machines available.</td>`;
          tbody.appendChild(row);
        } else {
          machines.forEach((machine) => {
            const row = document.createElement("tr");
            row.className = `machine-item ${machine.status.toLowerCase()}`;

            row.innerHTML = `
                                  <td>${machine.name}</td>
                                  <td>${machine.status}</td>
                                  <td>${machine.location}</td>
                                  <td><a href="/machine/${machine.id}" class="btn">View Details</a></td>
                              `;
            tbody.appendChild(row);
          });
        }
      })
      .catch((error) => {
        console.error("Error loading assigned machines:", error);
        // display an error message to the user
        const row = document.createElement("tr");
        row.innerHTML = `<td colspan="4">Error loading assigned machines. Please try again later.</td>`;
        tbody.appendChild(row);
      });
  }
