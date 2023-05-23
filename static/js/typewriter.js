// Get the page title element by its ID
const pageTitle = document.getElementById('page-title');

// Get the number of characters in the title
const titleLength = pageTitle.textContent.length;

// Set the animation steps dynamically
pageTitle.style.animation = `typing 2s steps(${titleLength}), blink .5s step-end infinite alternate`;
