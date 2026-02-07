document.addEventListener('DOMContentLoaded', function () {
    // --- Constants ---
    const WORLDS = ['City', 'Space', 'Game'];
    const ASSETS = {
        'City': { img: 'assets/city1.png', video: 'assets/city.mp4' },
        'Space': { img: 'assets/space.png', video: 'assets/space.mp4' },
        'Game': { img: 'assets/game.png', video: null }
    };

    // --- State ---
    let currentIndex = 0; // 0: City, 1: Space, 2: Game
    let isVideoPlaying = false;

    // --- DOM Elements ---
    const dashboardView = document.getElementById('dashboard');
    const videoPlayerView = document.getElementById('video-player');
    const bgImage = document.getElementById('bg-image');
    const videoElement = document.getElementById('main-video');
    const videoSource = document.getElementById('video-source');

    // --- Initialization ---
    function init() {
        updateDashboard();
        setupKeyHandlers();
        setupVideoEvents();
    }

    // --- Dashboard Logic ---
    function updateDashboard() {
        const currentWorld = WORLDS[currentIndex];
        const assetPath = ASSETS[currentWorld].img;
        bgImage.src = assetPath;
        console.log(`Switched to world: ${currentWorld}`);
    }

    function navigate(direction) {
        if (isVideoPlaying) return; // Prevent navigation while video plays

        if (direction === 'UP') {
            currentIndex = (currentIndex - 1 + WORLDS.length) % WORLDS.length;
        } else if (direction === 'DOWN') {
            currentIndex = (currentIndex + 1) % WORLDS.length;
        }
        updateDashboard();
    }

    // --- Video Logic ---
    function playVideo() {
        const currentWorld = WORLDS[currentIndex];
        const videoPath = ASSETS[currentWorld].video;

        if (!videoPath) {
            console.log('No video for this world');
            return;
        }

        isVideoPlaying = true;

        // Show Video View
        dashboardView.classList.remove('active');
        dashboardView.classList.add('hidden');
        videoPlayerView.classList.remove('hidden');
        videoPlayerView.classList.add('active');

        // Load and Play
        videoSource.src = videoPath;
        videoElement.load();
        videoElement.play().catch(e => console.error('Play error:', e));

        // Ensure focus is on video to capture back keys if needed? 
        // In simple vanilla JS, global key listener handles it.
    }

    function stopVideo() {
        if (!isVideoPlaying) return;

        videoElement.pause();
        videoElement.currentTime = 0;
        videoSource.src = ""; // Unload

        isVideoPlaying = false;

        // Restore Dashboard View
        videoPlayerView.classList.remove('active');
        videoPlayerView.classList.add('hidden');
        dashboardView.classList.remove('hidden');
        dashboardView.classList.add('active');

        // Ensure focus returns to dashboard context (if we were using spatial nav)
    }

    function setupVideoEvents() {
        videoElement.addEventListener('ended', function () {
            console.log('Video ended');
            stopVideo();
        });

        // Optional: Error handling
        videoElement.addEventListener('error', function (e) {
            console.error('Video error', e);
            stopVideo();
        });
    }

    // --- Input Handling ---
    function setupKeyHandlers() {
        document.addEventListener('keydown', function (e) {
            console.log('Key pressed:', e.keyCode, e.key);

            // Tizen Remote Keys (and simplified PC mapping)
            switch (e.keyCode) {
                case 38: // UP Arrow
                    navigate('UP');
                    break;
                case 40: // DOWN Arrow
                    navigate('DOWN');
                    break;
                case 13: // Enter / OK
                    if (!isVideoPlaying) {
                        playVideo();
                    }
                    break;
                case 10009: // Return / Back (Tizen Code)
                case 27:    // Esc (PC fallback)
                    if (isVideoPlaying) {
                        stopVideo();
                    }
                    break;
                default:
                    break;
            }
        });
    }

    init();
});
