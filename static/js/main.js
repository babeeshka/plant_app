document.addEventListener('DOMContentLoaded', function () {
    const pageTitle = document.querySelector('.page-title');
    if (pageTitle) {
        const textLength = pageTitle.textContent.length;
        pageTitle.classList.add('typing');
        pageTitle.style.width = `${textLength}ch`;
        pageTitle.style.animation = `typing ${textLength / 10}s steps(${textLength}), blink .5s step-end infinite alternate`;
    }
});
