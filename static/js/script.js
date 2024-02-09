function setTheme() {
  var currentTheme = localStorage.getItem("theme");
  if (currentTheme === "light") {
    localStorage.setItem("theme", "dark");
  } else {
    localStorage.setItem("theme", "light");
  }
  applyTheme();
}

function applyTheme() {
  var theme = localStorage.getItem("theme");
  document.documentElement.setAttribute("data-bs-theme", theme);
}
