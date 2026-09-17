const applicationForm =
    document.getElementById("applicationForm");

const successMessage =
    document.getElementById("successMessage");

const errorMessage =
    document.getElementById("errorMessage");


applicationForm.addEventListener("submit", async function(event) {

    event.preventDefault();


    // Get student name
    const studentName =
        document.getElementById("studentName").value.trim();


    // Check student name
    if (studentName === "") {

        errorMessage.textContent =
            "Please enter student name.";

        errorMessage.style.display = "block";

        successMessage.style.display = "none";

        return;
    }


    try {

        // Send ONLY student name to Flask
        const response = await fetch("/api/students", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                name: studentName
            })

        });


        // Get Flask response
        const data = await response.json();


        // Check if Flask returned an error
        if (!response.ok) {

            throw new Error(
                data.message || "Could not save student."
            );

        }


        // Show success message
        successMessage.textContent =
            "Application submitted successfully! Student ID: "
            + data.student.id;

        successMessage.style.display = "block";

        errorMessage.style.display = "none";


        // Clear form
        applicationForm.reset();

    }

    catch (error) {

        console.error("Error:", error);

        errorMessage.textContent =
            "Could not save student. Please try again.";

        errorMessage.style.display = "block";

        successMessage.style.display = "none";

    }

});