const applicationForm =
    document.getElementById("applicationForm");

const successMessage =
    document.getElementById("successMessage");


applicationForm.addEventListener("submit", function(event) {

    event.preventDefault();


    // Get form values

    const studentName =
        document.getElementById("studentName").value;

    const fatherName =
        document.getElementById("fatherName").value;

    const email =
        document.getElementById("email").value;

    const phone =
        document.getElementById("phone").value;

    const studentClass =
        document.getElementById("class").value;

    const message =
        document.getElementById("message").value;


    // Display submitted information in console

    console.log("Student Name:", studentName);

    console.log("Father's Name:", fatherName);

    console.log("Email:", email);

    console.log("Phone:", phone);

    console.log("Class:", studentClass);

    console.log("Additional Information:", message);


    // Show success message

    successMessage.style.display = "block";


    // Clear form

    applicationForm.reset();

});