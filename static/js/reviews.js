document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("toggleReviewBtn");
    const box = document.getElementById("reviewFormBox");

    btn.addEventListener("click", () => {
        box.classList.toggle("hidden");

        // change button text
        if (box.classList.contains("hidden")) {
            btn.textContent = "Write a review";
        } else {
            btn.textContent = "Hide form";
        }
    });
});
