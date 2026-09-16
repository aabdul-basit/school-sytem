// =========================
// THEME SYSTEM
// =========================

const themeBtn = document.getElementById("themeBtn");
const themeMenu = document.getElementById("themeMenu");

// Open / close theme menu
if (themeBtn) {
    themeBtn.addEventListener("click", () => {
        themeMenu.classList.toggle("show");
    });
}

// Change theme
function changeTheme(theme) {

    // Remove old theme
    document.body.classList.remove(
        "theme-blue",
        "theme-green",
        "theme-purple",
        "theme-orange",
        "theme-red",
        "theme-dark"
    );

    // Add selected theme
    document.body.classList.add("theme-" + theme);

    // Save theme
    localStorage.setItem("schoolTheme", theme);

    // Close menu
    themeMenu.classList.remove("show");
}

// Load saved theme
const savedTheme = localStorage.getItem("schoolTheme");

if (savedTheme) {
    document.body.classList.add("theme-" + savedTheme);
} else {
    document.body.classList.add("theme-blue");
}