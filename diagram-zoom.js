// Click a diagram to see it at viewport size (book.toml: additional-js).
//
// mermaid scales every SVG down to the reading column, and a nine-lane
// sequence diagram at 800px is unreadable. A click on any rendered diagram
// (or on a generated figure, `figure.map`) opens it in an overlay sized to
// the viewport, on the page's own background so the theme's colours still
// work; click anywhere or press Escape to close. Event delegation, because
// mermaid renders after this script runs.
(() => {
    const SELECTOR = 'pre.mermaid svg, figure.map svg';
    let overlay = null;

    function close() {
        if (!overlay) return;
        overlay.remove();
        overlay = null;
        document.removeEventListener('keydown', onKey);
    }

    function onKey(e) {
        if (e.key === 'Escape') close();
    }

    function open(svg) {
        close();
        overlay = document.createElement('div');
        overlay.className = 'diagram-lightbox';
        const panel = document.createElement('div');
        panel.className = 'diagram-lightbox-panel';
        const clone = svg.cloneNode(true);
        clone.removeAttribute('width');
        clone.removeAttribute('height');
        clone.style.maxWidth = 'none';
        clone.style.width = '100%';
        clone.style.height = 'auto';
        panel.appendChild(clone);
        overlay.appendChild(panel);
        overlay.addEventListener('click', close);
        document.body.appendChild(overlay);
        document.addEventListener('keydown', onKey);
    }

    document.addEventListener('click', (e) => {
        if (overlay || !e.target.closest) return;
        if (e.target.closest('a')) return;          // links inside a diagram stay links
        const svg = e.target.closest(SELECTOR);
        if (!svg) return;
        e.preventDefault();
        open(svg);
    });
})();
