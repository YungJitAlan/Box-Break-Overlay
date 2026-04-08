function launchConfetti() {
    script.onload = () => {
        confetti({
            particleCount: 120,
            spread: 80,
            origin: { y: 0.6 }
        });
    };

    document.body.appendChild(script);
}