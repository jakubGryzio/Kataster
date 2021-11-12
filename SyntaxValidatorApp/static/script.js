"use strict";

const btnClose = document.querySelector(".cancel");
const message = document.querySelector(".message")

btnClose.addEventListener("click", () => {
  message.classList.add("visuallyhidden");
});
