// The licence and the Mojang disclaimer, on every page (book.toml: additional-js).
//
// mdBook has no footer setting, so one is appended to each page's <main>.
// It belongs on every page rather than only in the introduction: the pages
// are meant to be linked to and quoted individually, and a reader who lands
// on `the-sword-swing` from a search should see what they may do with it and
// whose game it describes without going looking.
(() => {
    const FOOTER = `
      <p>Unofficial. Not endorsed by, sponsored by or associated with Mojang
      Studios or Microsoft; <em>Minecraft</em> is a trademark of Mojang
      Synergies AB. This book describes the game, and contains none of it.</p>
      <p>The writing and the figures are
      <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>
      &mdash; reuse them with credit to
      <a href="https://minecraftdocs.dev">minecraftdocs.dev</a>, and keep
      derivatives under the same licence. Corrections welcome on
      <a href="https://github.com/AlexanderjFraser/MinecraftDocs">GitHub</a>.</p>`;

    function add() {
        const main = document.querySelector('main');
        if (!main || main.querySelector('.site-footer')) return;
        const el = document.createElement('footer');
        el.className = 'site-footer';
        el.innerHTML = FOOTER;
        main.appendChild(el);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', add);
    } else {
        add();
    }
})();
