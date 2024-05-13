document.addEventListener('DOMContentLoaded', function () {
    const fullscreenBtns = document.querySelectorAll('.fullscreen-btn');

    fullscreenBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            const container = this.parentElement;

            if (!document.fullscreenElement) {
                if (container.requestFullscreen) {
                    container.requestFullscreen();
                } else if (container.webkitRequestFullscreen) { /* Safari */
                    container.webkitRequestFullscreen();
                } else if (container.msRequestFullscreen) { /* IE/Edge */
                    container.msRequestFullscreen();
                }
            } else {
                if (document.exitFullscreen) {
                    document.exitFullscreen();
                } else if (document.webkitExitFullscreen) { /* Safari */
                    document.webkitExitFullscreen();
                } else if (document.msExitFullscreen) { /* IE/Edge */
                    document.msExitFullscreen();
                }
            }
        });
    });
});
