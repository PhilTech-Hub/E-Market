document.addEventListener("DOMContentLoaded", function () {
  const loginButton = document.querySelector("#loginButton");
  if (loginButton) {
    loginButton.addEventListener("click", function (event) {
      // Prevent form submission if needed for validation or other logic
      // event.preventDefault();
      console.log("Login button clicked");
    });
  }
});

// Script to toggle between dark and light themes
document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM fully loaded and parsed.");
  console.log(document.body.innerHTML); // Log the full body HTML

  const themeToggleButton = document.getElementById("theme-toggle");
  const themeIcon = document.getElementById("theme-icon");

  console.log(themeToggleButton); // Check if this is null
  console.log(themeIcon); // Check if this is null

  if (themeToggleButton && themeIcon) {
    console.log("Theme toggle button and icon found.");

    // Check if the current theme is light or dark
    if (document.body.classList.contains("bg-dark")) {
      themeIcon.classList.remove("fa-sun");
      themeIcon.classList.add("fa-moon");
    }

    themeToggleButton.addEventListener("click", function () {
      document.body.classList.toggle("bg-light");
      document.body.classList.toggle("bg-dark");

      if (document.body.classList.contains("bg-dark")) {
        themeIcon.classList.remove("fa-sun");
        themeIcon.classList.add("fa-moon");
      } else {
        themeIcon.classList.remove("fa-moon");
        themeIcon.classList.add("fa-sun");
      }
    });
  } else {
    console.error("Theme toggle button or icon not found.");
  }
});

// Testimonial Slider JavaScript
let currentSlide = 0;

function changeSlide(index) {
  const slider = document.querySelector(".testimonial-slider");
  const dots = document.querySelectorAll(".slider-dots .dot");
  currentSlide = index;
  slider.style.transform = `translateX(-${index * 100}%)`;
  dots.forEach((dot) => dot.classList.remove("active"));
  dots[index].classList.add("active");
}

function nextSlide() {
  const totalSlides = document.querySelectorAll(".testimonial").length;
  currentSlide = (currentSlide + 1) % totalSlides;
  changeSlide(currentSlide);
}

function prevSlide() {
  const totalSlides = document.querySelectorAll(".testimonial").length;
  currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
  changeSlide(currentSlide);
}

//JS code of fading contents before reaching navbar
$(document).ready(function () {
  var navbarHeight = $(".navbar").outerHeight(); // Get the height of the navbar
  $(window).scroll(function () {
    var scrollPosition = $(window).scrollTop(); // Get the scroll position

    // If the scroll position is greater than the navbar height, add the fade-out class
    if (scrollPosition > navbarHeight) {
      $(".fade-on-scroll").addClass("fade-out");
    } else {
      $(".fade-on-scroll").removeClass("fade-out");
    }
  });
});

// Typing Effect JavaScript
document.addEventListener("DOMContentLoaded", function () {
  const headingText = "Welcome to E-Market"; // Passed dynamically from Flask
  const subheadingText = "Find the best products from trusted sellers worldwide."; // Passed dynamically from Flask
  const typingSpeed = 75; // Speed in milliseconds

  // Typing function
  function typeEffect(element, text, callback) {
    let i = 0;
    const timer = setInterval(() => {
      if (i < text.length) {
        element.innerHTML += text.charAt(i);
        i++;
      } else {
        clearInterval(timer);
        if (callback) callback(); // Call the next typing effect
      }
    }, typingSpeed);
  }

  // Start typing the heading, then the subheading
  const headingElement = document.getElementById("cta-heading");
  const subheadingElement = document.getElementById("cta-subheading");

  typeEffect(headingElement, headingText, () => {
    typeEffect(subheadingElement, subheadingText);
  });
});
