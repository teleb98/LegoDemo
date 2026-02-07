document.addEventListener('DOMContentLoaded', () => {
    const bgImage = document.getElementById('bg-image');
    // We could add a video element here if needed, but for now we just swap the BG
    // or we can reuse the existing video structure if we want to play videos.

    let currentTheme = 'default';

    // Theme Mapping
    const themeAssets = {
        'City': { img: 'assets/city1.png', video: 'assets/city.mp4' },
        'Creator': { img: 'assets/city1.png', video: 'assets/city.mp4' },
        'Architecture': { img: 'assets/city1.png', video: 'assets/city.mp4' },

        'Space': { img: 'assets/space.png', video: 'assets/space.mp4' },
        'Star Wars': { img: 'assets/space.png', video: 'assets/space.mp4' },

        'default': { img: 'assets/game.png', video: null }
    };

    function updateUI(theme, set_name) {
        console.log(`Updating UI to theme: ${theme}`);

        // Normalize theme key
        let assets = themeAssets['default'];

        // Simple fuzzy match or direct lookup
        for (const key in themeAssets) {
            if (theme.includes(key)) {
                assets = themeAssets[key];
                break;
            }
        }

        // Update Background
        bgImage.src = assets.img;

        // Optional: Show a toast or overlay with the detected set name
        // (Not implementing full video player switch here to keep it simple, 
        // effectively just changing the "ambient mode" background)
    }

    async function pollState() {
        try {
            const response = await fetch('/api/state');
            const state = await response.json();

            if (state.current_theme && state.current_theme !== currentTheme) {
                currentTheme = state.current_theme;
                updateUI(currentTheme, state.detected_set);
            }
        } catch (error) {
            console.error("Error polling state:", error);
        }
    }

    // Poll every 2 seconds
    setInterval(pollState, 2000);
});
