document.addEventListener('DOMContentLoaded', () => {
    const bgImage = document.getElementById('bg-image');
    const dashboard = document.getElementById('dashboard');
    const videoPlayerView = document.getElementById('video-player');
    const videoElement = document.getElementById('main-video');
    const videoSource = document.getElementById('video-source');

    let currentTheme = 'default';

    // Theme Mapping
    const themeAssets = {
        'City': { img: 'assets/city1.png', video: 'assets/city.mp4' },
        'Creator': { img: 'assets/city1.png', video: 'assets/city.mp4' },
        'Architecture': { img: 'assets/city1.png', video: 'assets/city.mp4' },

        'Space': { img: 'assets/space.png', video: 'assets/space.mp4' },
        'Star Wars': { img: 'assets/space.png', video: 'assets/space.mp4' },

        'Game': { img: 'assets/game.png', video: null }, // Added Game theme
        'default': { img: 'assets/game.png', video: null }
    };

    // Navigation Order for Remote
    const displayThemes = ['City', 'Space', 'Game'];
    let navIndex = 0;

    function updateUI(theme) {
        console.log(`Updating UI to theme: ${theme}`);
        currentTheme = theme;

        let assets = themeAssets['default'];

        // Fuzzy match
        for (const key in themeAssets) {
            if (theme.includes(key)) {
                assets = themeAssets[key];
                break;
            }
        }

        // Update Background
        bgImage.src = assets.img;
    }

    // --- Video Logic ---
    function playVideo() {
        let assets = themeAssets['default'];
        for (const key in themeAssets) {
            if (currentTheme.includes(key)) {
                assets = themeAssets[key];
                break;
            }
        }

        if (assets.video) {
            console.log(`Playing video: ${assets.video}`);
            videoSource.src = assets.video;
            videoElement.load();

            dashboard.classList.add('hidden');
            dashboard.classList.remove('active');

            videoPlayerView.classList.add('active');
            videoPlayerView.classList.remove('hidden');

            videoElement.play().catch(e => console.error("Play error:", e));

            // Auto-return when ended
            videoElement.onended = stopVideo;
        } else {
            console.log("No video for this theme");
        }
    }

    function stopVideo() {
        console.log("Stopping video");
        videoElement.pause();
        videoSource.src = "";

        videoPlayerView.classList.add('hidden');
        videoPlayerView.classList.remove('active');

        dashboard.classList.add('active');
        dashboard.classList.remove('hidden');
    }

    // --- Remote Control Logic ---
    document.addEventListener('keydown', (e) => {
        console.log('Key pressed:', e.keyCode);

        switch (e.keyCode) {
            case 38: // UP Arrow
                navIndex = (navIndex - 1 + displayThemes.length) % displayThemes.length;
                updateUI(displayThemes[navIndex]);
                break;

            case 40: // DOWN Arrow
                navIndex = (navIndex + 1) % displayThemes.length;
                updateUI(displayThemes[navIndex]);
                break;

            case 13: // ENTER
                playVideo();
                break;

            case 10009: // RETURN / BACK (Tizen)
            case 27:    // ESC (PC)
                stopVideo();
                break;
        }
    });

    // --- AI Polling Logic ---
    async function pollState() {
        try {
            const response = await fetch('/api/state');
            const state = await response.json();

            if (state.current_theme && state.current_theme !== currentTheme) {
                // If AI detects a change, it overrides manual navigation
                updateUI(state.current_theme);

                // Sync navIndex to match AI theme if possible
                const matchIndex = displayThemes.findIndex(t => state.current_theme.includes(t));
                if (matchIndex !== -1) {
                    navIndex = matchIndex;
                }
            }
        } catch (error) {
            console.error("Error polling state:", error);
        }
    }

    // Poll every 2 seconds
    setInterval(pollState, 2000);
});
