(function() {
    const contentDiv = document.getElementById('content');
    let lastContent = contentDiv.innerHTML;
    let animationApplied = false;

    async function fetchHTML() {
        try {
            const response = await fetch('box_report.html', { cache: 'no-store' });
            if (response.ok) {
                const text = await response.text();
                const parser = new DOMParser();
                const doc = parser.parseFromString(text, 'text/html');
                const newContent = doc.getElementById('content').innerHTML;
                if (newContent !== lastContent) {
                    lastContent = newContent;
                    contentDiv.innerHTML = newContent;
                    adjustScrolling();
                }
            }
        } catch (error) {
            console.error('Error fetching HTML:', error);
        }
    }

    function adjustScrolling() {
        // Remove any existing animation
        contentDiv.style.animation = 'none';
        // Allow the browser to apply the removal
        requestAnimationFrame(() => {
            // Check if content height exceeds viewport height
            const contentHeight = contentDiv.scrollHeight;
            const viewportHeight = window.innerHeight;
            if (contentHeight > viewportHeight) {
                // Apply scrolling animation
                contentDiv.style.animation = 'scrollUp 30s linear infinite';
                animationApplied = true;
            } else {
                // Ensure content is positioned statically
                contentDiv.style.position = 'static';
                contentDiv.style.animation = 'none';
                animationApplied = false;
            }
        });
    }

    function restartAnimation() {
        if (animationApplied) {
            // Temporarily disable animation
            contentDiv.style.animation = 'none';
            // Trigger reflow to restart animation
            void contentDiv.offsetWidth;
            // Re-enable animation
            contentDiv.style.animation = 'scrollUp 30s linear infinite';
        }
    }

    // Initial adjustment on load
    window.addEventListener('load', adjustScrolling);
    // Adjust on window resize
    window.addEventListener('resize', adjustScrolling);
    // Fetch updates periodically
    setInterval(fetchHTML, 5000); // Check for updates every 5 seconds
})();