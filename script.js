document.addEventListener('DOMContentLoaded', function () {
    const fullscreenBtns = document.querySelectorAll('.fullscreen-btn');

    fullscreenBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            const container = this.parentElement;
            if (container.requestFullscreen) {
                container.requestFullscreen();
            } else if (container.webkitRequestFullscreen) { /* Safari */
                container.webkitRequestFullscreen();
            } else if (container.msRequestFullscreen) { /* IE/Edge */
                container.msRequestFullscreen();
            }
        });
    });
});