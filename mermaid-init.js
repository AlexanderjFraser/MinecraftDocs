// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.
//
// Derived from the file `mdbook-mermaid install` writes (MPL-2.0): the theme-toggle
// reload below is its logic, kept. Everything else is MinecraftDocs' own figure theme,
// adopted by pass 7, session A (2026-09-15) and measured before and after.
//
// What the shipped default did, and why it is gone: `mermaid.initialize({ startOnLoad, theme })`
// is mermaid's own lilac palette in Trebuchet with **no wrapping**, and a sequence diagram with
// no wrapping is as wide as its longest message between two lanes. Over the 194 mermaid figures
// that put 134 of them below their natural size, 76 below half, and 89 showing type under 9px —
// the widest 5,415px, shown at a fifth. This file changes four things and no page:
//
//   1. the site's own font (Open Sans, what mdBook sets on the body) at a 16px base;
//   2. `sequence.wrap` at a 180px message width, so lanes stay a fixed distance apart and a long
//      message wraps instead of pushing them out; `mirrorActors: false` drops the second row of
//      participant boxes at the foot, a screen away on a twenty-message trace;
//   3. the `base` theme with variables read off mdBook's light and navy palettes, so a figure
//      looks like part of the page in both, rather than mermaid's lilac in both;
//   4. flowchart labels wrap at 220px and edges curve gently.
//
// Measured over the corpus (render_figures.js, Chrome, the 1,092px column, light): the sequence
// diagrams go from 70 below half to none and from 76 with type under 9px to none; over all
// figures the median scale is 0.61 → 0.82 and 89 under 9px → 10. The cost is height (the median
// sequence diagram 401px → 940px) and that mermaid hyphen-breaks a word wider than the wrap
// width — which is why a lane name longer than the box carries its own `<br/>` at a CamelCase
// boundary (TEMPLATE.md, *Figures*), and why the label budgets are a rule and not a taste.
//
// The whole visual grammar lives here and in custom.css: `%%{init}%%`, `classDef`, `style` and
// `linkStyle` do not go in a page. Do not re-run `mdbook-mermaid install` — it overwrites this
// file with the default. `node tools/render_figures.js` is how a change to it is argued.
(() => {
    const darkThemes = ['ayu', 'navy', 'coal'];
    const lightThemes = ['light', 'rust'];

    const classList = document.getElementsByTagName('html')[0].classList;

    let lastThemeWasLight = true;
    for (const cssClass of classList) {
        if (darkThemes.includes(cssClass)) {
            lastThemeWasLight = false;
            break;
        }
    }

    const font = '"Open Sans", "Segoe UI", Helvetica, Arial, sans-serif';

    // The palettes are mdBook's own: the light theme's page white and link blue, the navy
    // theme's surface and text. The five semantic classes (server · client · netty · worker ·
    // disk) are in custom.css, not here, because a class is a stylesheet rule and follows the
    // theme without a second render.
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

    // Simplest way to make mermaid re-render the diagrams in the new theme is via refreshing the page

    for (const darkTheme of darkThemes) {
        const el = document.getElementById('mdbook-theme-' + darkTheme);
        if (el) el.addEventListener('click', () => { if (lastThemeWasLight) window.location.reload(); });
    }

    for (const lightTheme of lightThemes) {
        const el = document.getElementById('mdbook-theme-' + lightTheme);
        if (el) el.addEventListener('click', () => { if (!lastThemeWasLight) window.location.reload(); });
    }
})();
