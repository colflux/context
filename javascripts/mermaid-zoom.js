document.addEventListener("click", function (e) {
  var el = e.target.closest(".mermaid");
  if (!el) return;
  el.classList.toggle("mermaid-zoomed");
});

document.addEventListener("keydown", function (e) {
  if (e.key === "Escape") {
    document.querySelectorAll(".mermaid-zoomed").forEach(function (el) {
      el.classList.remove("mermaid-zoomed");
    });
  }
});
