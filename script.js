document.querySelector('.scroll-button.prev').addEventListener('click', function () {
    document.querySelector('.scroll-container').scrollBy({
        left: -window.innerWidth,
        behavior: 'smooth'
    });
});

document.querySelector('.scroll-button.next').addEventListener('click', function () {
    document.querySelector('.scroll-container').scrollBy({
        left: window.innerWidth,
        behavior: 'smooth'
    });
});
