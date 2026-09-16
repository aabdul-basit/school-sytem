// ======================================
// Course Data
// ======================================

const courses = [

    {
        name: "Computer Science",
        teacher: "Mr. Ahmed Khan",
        duration: 12,
        icon: "💻",
        description: "Learn programming, computer fundamentals, databases, and software development."
    },

    {
        name: "Mathematics",
        teacher: "Ail khan  ",
        duration: 6,
        icon: "📐",
        description: "Develop strong mathematical skills through practical problems and exercises."
    },

    {
        name: "English Language",
        teacher: "Mr. Hassan Shah",
        duration: 6,
        icon: "📖",
        description: "Improve grammar, vocabulary, speaking, writing, and communication skills."
    },

    {
        name: "Physics",
        teacher: "Dr. Usman Khan",
        duration: 12,
        icon: "⚛️",
        description: "Understand the fundamental principles of physics through theory and experiments."
    },

    {
        name: "Web Development",
        teacher: "Mr. Bilal Ahmed",
        duration: 6,
        icon: "🌐",
        description: "Learn HTML, CSS, JavaScript, and the fundamentals of modern web development."
    },

    {
        name: "Graphic Design",
        teacher: "Ms. Ayesha Noor",
        duration: 3,
        icon: "🎨",
        description: "Learn design principles, visual communication, and creative digital design."
    },

    {
        name: "Database Management",
        teacher: "Mr. Hamza Khan",
        duration: 6,
        icon: "🗄️",
        description: "Learn databases, SQL, tables, relationships, queries, and database management."
    },

    {
        name: "Computer Networking",
        teacher: "Mr. Salman Ahmad",
        duration: 6,
        icon: "🌐",
        description: "Learn networking fundamentals, protocols, devices, IP addressing, and security."
    },

    {
        name: "Artificial Intelligence",
        teacher: "Dr. Umar Farooq",
        duration: 12,
        icon: "🤖",
        description: "Explore artificial intelligence, machine learning concepts, and intelligent systems."
    }

];


// ======================================
// HTML Elements
// ======================================

const coursesContainer = document.getElementById("coursesContainer");

const searchInput = document.getElementById("searchInput");

const durationFilter = document.getElementById("durationFilter");

const noResults = document.getElementById("noResults");


// ======================================
// Display Courses
// ======================================

function displayCourses(courseList) {

    coursesContainer.innerHTML = "";


    if (courseList.length === 0) {

        noResults.style.display = "block";

        return;
    }


    noResults.style.display = "none";


    courseList.forEach(course => {

        const courseCard = document.createElement("div");

        courseCard.className = "course-card";


        courseCard.innerHTML = `

            <div class="course-icon">
                ${course.icon}
            </div>

            <h2>${course.name}</h2>

            <p class="course-description">
                ${course.description}
            </p>

            <div class="course-info">

                <div class="info-row">
                    <span class="info-label">
                        Teacher
                    </span>

                    <span class="info-value">
                        ${course.teacher}
                    </span>
                </div>


                <div class="info-row">
                    <span class="info-label">
                        Duration
                    </span>

                    <span class="duration">
                        ${course.duration} Months
                    </span>
                </div>

            </div>

        `;


        coursesContainer.appendChild(courseCard);

    });

}


// ======================================
// Search & Filter
// ======================================

function filterCourses() {

    const searchText = searchInput.value.toLowerCase();

    const selectedDuration = durationFilter.value;


    const filteredCourses = courses.filter(course => {

        const matchesSearch =
            course.name.toLowerCase().includes(searchText) ||
            course.teacher.toLowerCase().includes(searchText);


        const matchesDuration =
            selectedDuration === "all" ||
            course.duration.toString() === selectedDuration;


        return matchesSearch && matchesDuration;

    });


    displayCourses(filteredCourses);

}


// ======================================
// Events
// ======================================

searchInput.addEventListener("input", filterCourses);

durationFilter.addEventListener("change", filterCourses);


// ======================================
// Mobile Menu
// ======================================

function toggleMenu() {

    const navLinks = document.querySelector(".nav-links");

    navLinks.classList.toggle("show");

}


// ======================================
// Load Courses
// ======================================

displayCourses(courses);