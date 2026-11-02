document.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-toggle-password]");
    if (!btn) return;
    const input = btn.parentElement.querySelector("input");
    const svg = btn.querySelectorAll("svg");
    const visible = input.type === "password";0

    input.type = visible ? "text" : "password";

    svg[0].classList.toggle( "hidden");
    svg[1].classList.toggle("hidden");

});