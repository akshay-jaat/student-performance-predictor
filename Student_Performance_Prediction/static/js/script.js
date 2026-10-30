document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("predictionForm");
  if (form) {
    form.addEventListener("submit", () => {
      const button = form.querySelector("button[type='submit']");
      if (button) {
        button.disabled = true;
        button.innerHTML = "Analysing your details...";
      }
    });
  }
});
