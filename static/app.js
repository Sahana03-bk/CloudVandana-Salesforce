const objectSelect =
    document.getElementById("objectSelect");

const tableHead =
    document.getElementById("tableHead");

const tableBody =
    document.getElementById("tableBody");

const recordCount =
    document.getElementById("recordCount");

const loading =
    document.getElementById("loading");

const createButton =
    document.getElementById("createButton");

const modal =
    document.getElementById("modal");

const modalTitle =
    document.getElementById("modalTitle");

const closeModal =
    document.getElementById("closeModal");

const cancelButton =
    document.getElementById("cancelButton");

const recordForm =
    document.getElementById("recordForm");

const formFields =
    document.getElementById("formFields");

const tableContainer =
    document.getElementById("tableContainer");

const message =
    document.getElementById("message");


let currentObject =
    objectSelect.value;

let records = [];

let offset = 0;

let totalSize = 0;

let loadingRecords = false;

let editingRecord = null;


// Salesforce fields

const objectFields = {

    Account: [
        "Id",
        "Name",
        "Type",
        "Industry",
        "Phone"
    ],

    Opportunity: [
        "Id",
        "Name",
        "StageName",
        "CloseDate",
        "Amount"
    ],

    Lead: [
        "Id",
        "FirstName",
        "LastName",
        "Company",
        "Email"
    ],

    Contact: [
        "Id",
        "FirstName",
        "LastName",
        "Email",
        "Phone"
    ],

    Case: [
    "Id",
    "CaseNumber",
    "Subject",
    "Status",
    "Priority",
    "Origin"
]
};


// ----------------------------------------
// Load records
// ----------------------------------------

async function loadRecords(reset = false) {

    if (loadingRecords) {
        return;
    }

    if (
        !reset &&
        records.length >= totalSize &&
        totalSize !== 0
    ) {
        return;
    }

    loadingRecords = true;

    loading.style.display = "inline";

    if (reset) {

        records = [];

        offset = 0;

        totalSize = 0;

        tableBody.innerHTML = "";
    }

    try {

        const response = await fetch(
            `/records/${currentObject}?offset=${offset}`
        );

        const data = await response.json();

        if (!response.ok) {

            throw new Error(
                data.detail || "Failed to load records"
            );
        }

        totalSize = data.totalSize;

        records = [
            ...records,
            ...data.records
        ];

        renderTable();

        offset += data.records.length;

    } catch (error) {

        showMessage(
            error.message,
            true
        );

    } finally {

        loadingRecords = false;

        loading.style.display = "none";
    }
}


// ----------------------------------------
// Render table
// ----------------------------------------

function renderTable() {

    const fields =
        objectFields[currentObject];

    tableHead.innerHTML = "";

    const headerRow =
        document.createElement("tr");

    fields.forEach(field => {

        const th =
            document.createElement("th");

        th.textContent = field;

        headerRow.appendChild(th);
    });


    const actionHeader =
        document.createElement("th");

    actionHeader.textContent = "Actions";

    headerRow.appendChild(actionHeader);

    tableHead.appendChild(headerRow);


    tableBody.innerHTML = "";


    records.forEach(record => {

        const row =
            document.createElement("tr");

        fields.forEach(field => {

            const cell =
                document.createElement("td");

            cell.textContent =
                record[field] ?? "";

            row.appendChild(cell);
        });


        const actionCell =
            document.createElement("td");


        const editButton =
            document.createElement("button");

        editButton.textContent = "Edit";

        editButton.className =
            "action-button edit-button";

        editButton.onclick = () =>
            openEditModal(record);


        const deleteButton =
            document.createElement("button");

        deleteButton.textContent = "Delete";

        deleteButton.className =
            "action-button delete-button";

        deleteButton.onclick = () =>
            deleteRecord(record.Id);


        actionCell.appendChild(editButton);

        actionCell.appendChild(deleteButton);

        row.appendChild(actionCell);

        tableBody.appendChild(row);
    });


    recordCount.textContent =
        `${records.length} of ${totalSize} records`;
}


// ----------------------------------------
// Object change
// ----------------------------------------

objectSelect.addEventListener(
    "change",
    () => {

        currentObject =
            objectSelect.value;

        loadRecords(true);
    }
);


// ----------------------------------------
// Create modal
// ----------------------------------------

createButton.addEventListener(
    "click",
    () => {

        editingRecord = null;

        modalTitle.textContent =
            `Create ${currentObject}`;

        buildForm();

        modal.classList.remove("hidden");
    }
);


// ----------------------------------------
// Edit modal
// ----------------------------------------

function openEditModal(record) {

    editingRecord = record;

    modalTitle.textContent =
        `Edit ${currentObject}`;

    buildForm(record);

    modal.classList.remove("hidden");
}


// ----------------------------------------
// Build dynamic form
// ----------------------------------------

function buildForm(record = {}) {

    formFields.innerHTML = "";

    const fields =
        objectFields[currentObject];

    fields.forEach(field => {

        if (
            field === "Id" ||
            field === "CaseNumber"
        ) {
            return;
        }

        const wrapper =
            document.createElement("div");

        wrapper.className =
            "form-field";


        const label =
            document.createElement("label");

        label.textContent =
            field;


        const input =
            document.createElement("input");

        input.name = field;

        input.value =
            record[field] ?? "";


        if (
            field === "CloseDate"
        ) {
            input.type = "date";
        } else if (
            field === "Amount"
        ) {
            input.type = "number";
        } else if (
            field === "Email"
        ) {
            input.type = "email";
        } else {
            input.type = "text";
        }


        wrapper.appendChild(label);

        wrapper.appendChild(input);

        formFields.appendChild(wrapper);
    });
}


// ----------------------------------------
// Save record
// ----------------------------------------

recordForm.addEventListener(
    "submit",
    async (event) => {

        event.preventDefault();

        const data = {};

        const inputs =
            formFields.querySelectorAll("input");

        inputs.forEach(input => {

            if (
                input.value.trim() !== ""
            ) {

                data[input.name] =
                    input.value;
            }
        });


        try {

            let response;


            if (editingRecord) {

                response = await fetch(
                    `/records/${currentObject}/${editingRecord.Id}`,
                    {
                        method: "PATCH",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(data)
                    }
                );

            } else {

                response = await fetch(
                    `/records/${currentObject}`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(data)
                    }
                );
            }


            const result =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    result.detail ||
                    "Operation failed"
                );
            }


            modal.classList.add("hidden");

            showMessage(
                editingRecord
                    ? "Record updated successfully."
                    : "Record created successfully."
            );


            await loadRecords(true);

        } catch (error) {

            showMessage(
                error.message,
                true
            );
        }
    }
);


// ----------------------------------------
// Delete
// ----------------------------------------

async function deleteRecord(recordId) {

    const confirmed =
        confirm(
            `Delete this ${currentObject} record?`
        );

    if (!confirmed) {
        return;
    }


    try {

        const response =
            await fetch(
                `/records/${currentObject}/${recordId}`,
                {
                    method: "DELETE"
                }
            );


        const result =
            await response.json();


        if (!response.ok) {

            throw new Error(
                result.detail ||
                "Delete failed"
            );
        }


        showMessage(
            "Record deleted successfully."
        );


        await loadRecords(true);

    } catch (error) {

        showMessage(
            error.message,
            true
        );
    }
}


// ----------------------------------------
// Modal close
// ----------------------------------------

function closeModalWindow() {

    modal.classList.add("hidden");

    editingRecord = null;
}

closeModal.onclick =
    closeModalWindow;

cancelButton.onclick =
    closeModalWindow;


// ----------------------------------------
// Infinite scroll
// ----------------------------------------

tableContainer.addEventListener(
    "scroll",
    () => {

        const nearBottom =
            tableContainer.scrollTop +
            tableContainer.clientHeight >=
            tableContainer.scrollHeight - 100;


        if (nearBottom) {

            loadRecords(false);
        }
    }
);


// ----------------------------------------
// Messages
// ----------------------------------------

function showMessage(
    text,
    isError = false
) {

    message.textContent = text;

    message.style.display = "block";

    message.style.background =
        isError
            ? "#ffe5e5"
            : "#e5f6e9";

    message.style.color =
        isError
            ? "#ba0517"
            : "#1b5e20";


    setTimeout(
        () => {
            message.style.display =
                "none";
        },
        4000
    );
}


// ----------------------------------------
// Initial load
// ----------------------------------------

loadRecords(true);