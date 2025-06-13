// MathJax Configuration for ContextCraft Documentation

window.MathJax = {
    tex: {
        inlineMath: [["\\(", "\\)"]],
        displayMath: [["\\[", "\\]"]],
        processEscapes: true,
        processEnvironments: true,
        tags: 'ams',
        packages: {'[+]': ['ams', 'color', 'cancel']}
    },
    options: {
        ignoreHtmlClass: ".*|",
        processHtmlClass: "arithmatex"
    },
    startup: {
        ready: function() {
            MathJax.startup.defaultReady();
            console.log('MathJax is ready for ContextCraft documentation! 📊');
        }
    },
    svg: {
        fontCache: 'global'
    }
};
