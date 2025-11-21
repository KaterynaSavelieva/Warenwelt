// register.js
// Logic for:
// 1) show/hide birthdate / company number by "kind"
// 2) toggle password visibility for two password fields
// 3) set max date for birthdate (today - 18 years)

document.addEventListener("DOMContentLoaded", () => {
  // ========== 1) Show/hide private / company fields ==========
  const kindSelect   = document.getElementById("kind-select");
  const birthGroup   = document.getElementById("birthdate-group");
  const companyGroup = document.getElementById("company-group");

  function updateKindFields() {
    if (!kindSelect || !birthGroup || !companyGroup) return;

    const kind = kindSelect.value;

    if (kind === "private") {
      birthGroup.style.display   = "block";
      companyGroup.style.display = "none";
    } else {
      birthGroup.style.display   = "none";
      companyGroup.style.display = "block";
    }
  }

  if (kindSelect) {
    kindSelect.addEventListener("change", updateKindFields);
    updateKindFields();  // initial state on page load
  }

  // ========== 2) Password eye toggle for two fields ==========
  function setupEye(inputId) {
    const input = document.getElementById(inputId);
    const eye   = document.querySelector(`.password-eye[data-target="${inputId}"]`);

    if (!input || !eye) return;

    eye.addEventListener("click", () => {
      if (input.type === "password") {
        input.type = "text";
        eye.textContent = "🙈";  // icon when password is visible
      } else {
        input.type = "password";
        eye.textContent = "👁️"; // icon when password is hidden
      }
    });
  }

  setupEye("password");
  setupEye("password2");

  // ========== 3) Max birthdate: today - 18 years ==========
  const bdInput = document.getElementById("birthdate");
  if (bdInput) {
    const today = new Date();
    const year  = today.getFullYear() - 18;
    const month = String(today.getMonth() + 1).padStart(2, "0");
    const day   = String(today.getDate()).padStart(2, "0");
    const maxDate = `${year}-${month}-${day}`;
    bdInput.setAttribute("max", maxDate);
  }
});
