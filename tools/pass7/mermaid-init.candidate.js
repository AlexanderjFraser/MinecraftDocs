// A candidate mermaid-init.js for pass 7's session A to judge (tools/pass7/, planning session 2026-09-14).
//
// The site ships mdbook-mermaid's default init: `mermaid.initialize({ startOnLoad: true, theme })`,
// which is mermaid's own palette in Trebuchet, and — the part that matters — no wrapping: a
// sequence diagram is as wide as its longest message between two lanes, so a seven-lane trace
// with forty-word messages renders at 4,000px and is shown at a quarter of its size (render/
// index.json: 134 of 194 figures shrunk, 89 with type under 9px). This file changes four things
// and nothing about any page:
//   1. the site's own font (Open Sans, what mdBook sets on the body) and a 16px base;
//   2. `sequence.wrap: true` with a 180px message width, so lanes stay a fixed distance apart and
//      long messages wrap instead of pushing the lanes out; `mirrorActors: false` drops the second
//      row of participant boxes at the foot, which on a 20-message trace is a screen away;
//   3. the `base` theme with variables read off mdBook's light and navy palettes, so a figure looks
//      like part of the page in both, instead of mermaid's lilac in both;
//   4. flowchart labels wrap at 220px (mermaid's default is 200) and edges curve gently.
// Try it without touching the site:
//     node tools/render_figures.js --no-build --out render/candidate --init-js tools/pass7/mermaid-init.candidate.js --css tools/pass7/figure-classes.candidate.css
// and compare render/candidate/index.json with render/index.json (scale, fonts.min). To adopt it,
// copy it over mermaid-init.js at the repo root (gitignored today, because mdbook-mermaid
// writes it; adopting means committing it and dropping it from .gitignore).
(() => {
    const darkThemes = ['ayu', 'navy', 'coal'];
    const lightThemes = ['light', 'rust'];
    const classList = document.getElementsByTagName('html')[0].classList;
    let lastThemeWasLight = true;
    for (const cssClass of classList) {
        if (darkThemes.includes(cssClass)) { lastThemeWasLight = false; break; }
    }
    const font = '"Open Sans", "Segoe UI", Helvetica, Arial, sans-serif';
    const light = {
        fontFamily: font, fontSize: '16px',
        background: '#ffffff', mainBkg: '#eef3fb', primaryColor: '#eef3fb', primaryTextColor: '#1d2733', primaryBorderColor: '#7d9cc9',
        secondaryColor: '#f6f1e4', secondaryTextColor: '#1d2733', secondaryBorderColor: '#c9b98a',
        tertiaryColor: '#f4f5f7', tertiaryTextColor: '#1d2733', tertiaryBorderColor: '#c8cdd3',
        lineColor: '#5c6b7a', textColor: '#1d2733', nodeBorder: '#7d9cc9', nodeTextColor: '#1d2733',
        clusterBkg: '#f7f8fa', clusterBorder: '#c8cdd3', titleColor: '#1d2733', edgeLabelBackground: '#ffffff',
        actorBkg: '#eef3fb', actorBorder: '#7d9cc9', actorTextColor: '#1d2733', actorLineColor: '#b3bcc7',
        signalColor: '#3a4653', signalTextColor: '#1d2733', labelBoxBkgColor: '#f4f5f7', labelBoxBorderColor: '#9aa7b5',
        labelTextColor: '#1d2733', loopTextColor: '#1d2733', noteBkgColor: '#fff6cc', noteBorderColor: '#e0c96a', noteTextColor: '#2b2b2b',
        activationBkgColor: '#e3ebf7', activationBorderColor: '#7d9cc9', sequenceNumberColor: '#ffffff',
    };
    const dark = {
        fontFamily: font, fontSize: '16px',
        background: '#161923', mainBkg: '#26304a', primaryColor: '#26304a', primaryTextColor: '#dfe3ee', primaryBorderColor: '#6f8fc4',
        secondaryColor: '#33302a', secondaryTextColor: '#dfe3ee', secondaryBorderColor: '#8a7d3a',
        tertiaryColor: '#1f2432', tertiaryTextColor: '#dfe3ee', tertiaryBorderColor: '#3d465c',
        lineColor: '#9aa7c2', textColor: '#dfe3ee', nodeBorder: '#6f8fc4', nodeTextColor: '#dfe3ee',
        clusterBkg: '#1c2130', clusterBorder: '#3d465c', titleColor: '#dfe3ee', edgeLabelBackground: '#161923',
        actorBkg: '#26304a', actorBorder: '#6f8fc4', actorTextColor: '#dfe3ee', actorLineColor: '#556077',
        signalColor: '#c5ccdb', signalTextColor: '#dfe3ee', labelBoxBkgColor: '#1f2432', labelBoxBorderColor: '#556077',
        labelTextColor: '#dfe3ee', loopTextColor: '#dfe3ee', noteBkgColor: '#3a3620', noteBorderColor: '#8a7d3a', noteTextColor: '#efe9c8',
        activationBkgColor: '#2f3b5a', activationBorderColor: '#6f8fc4', sequenceNumberColor: '#161923',
    };
    mermaid.initialize({
        startOnLoad: true,
        theme: 'base',
        themeVariables: lastThemeWasLight ? light : dark,
        fontFamily: font,
        flowchart: { htmlLabels: true, curve: 'basis', useMaxWidth: true, padding: 10, nodeSpacing: 32, rankSpacing: 44, wrappingWidth: 220 },
        sequence: { useMaxWidth: true, wrap: true, width: 180, messageMargin: 32, actorMargin: 48, boxMargin: 8, noteMargin: 8,
                    mirrorActors: false, diagramMarginX: 8, diagramMarginY: 8, actorFontSize: 15, messageFontSize: 15, noteFontSize: 14 },
        state: { useMaxWidth: true },
    });
    // mermaid renders once, into the theme it was given; the simplest way to re-render in the new theme is a reload.
    for (const darkTheme of darkThemes) {
        const el = document.getElementById('mdbook-theme-' + darkTheme);
        if (el) el.addEventListener('click', () => { if (lastThemeWasLight) window.location.reload(); });
    }
    for (const lightTheme of lightThemes) {
        const el = document.getElementById('mdbook-theme-' + lightTheme);
        if (el) el.addEventListener('click', () => { if (!lastThemeWasLight) window.location.reload(); });
    }
})();
