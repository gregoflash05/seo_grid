const togglers = document.querySelectorAll(".sidebar-toggler");
togglers.forEach((toggler) => {
  toggler.addEventListener("click", (e) => {
    document
      .querySelector("aside.sidebar")
      .parentElement.classList.toggle("collapsed-sidebar");
  });
});
