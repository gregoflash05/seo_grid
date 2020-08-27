const togglers = document.querySelectorAll(".sidebar-toggler");
togglers.forEach((toggler) => {
  toggler.addEventListener("click", (e) => {
    document
      .querySelector("aside.sidebar")
      .parentElement.classList.toggle("collapsed-sidebar");
  });
});
// Dropdown
const dropdownBtn = document.querySelector("#dropdownBtn");
const dropdown = document.querySelector(".dropdown-holder");
dropdownBtn.addEventListener("click", (e) => {
  dropdown.classList.toggle("closed");
});
// Click Ouside
var specifiedElement = document.querySelector(".avatar-section");

//I'm using "click" but it works with any event
document.addEventListener("click", function (event) {
  var isClickInside = specifiedElement.contains(event.target);

  !isClickInside && dropdown.classList.add("closed");
});
