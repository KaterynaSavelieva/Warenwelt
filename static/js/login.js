// Toggle password visibility on the login page
document.addEventListener("DOMContentLoaded", () => {
    console.log("login.js loaded");   // тимчасово, щоб бачити в консолі

    // 1) Find password field and eye icon
    const pwd = document.getElementById("password");
    const toggle = document.getElementById("togglePassword");

    // 2) If one of them is missing (on other pages) – do nothing
    if (!pwd || !toggle) {
        console.log("No password or toggle element found");
        return;
    }

    // 3) When user clicks the eye – switch input type and icon
    toggle.addEventListener("click", () => {
        if (pwd.type === "password") {
            pwd.type = "text";
            toggle.textContent = "🙈";  // icon when password is visible
        } else {
            pwd.type = "password";
            toggle.textContent = "👁️";  // icon when password is hidden
        }
    });
});
