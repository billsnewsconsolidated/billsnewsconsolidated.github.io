/* Bills News Consolidated — shared JS.
   Renders article cards (homepage), the hero, writer "filed under" lists,
   and full article pages from articles.json. No dependencies. */

(function () {
  'use strict';

  var DESKS = {
    'news':           { label: 'News',           cardClass: '',         kickerClass: '' },
    'film-room':      { label: 'Film Room',      cardClass: 'film',     kickerClass: 'film' },
    'culture-desk':   { label: 'Culture Desk',   cardClass: 'culture',  kickerClass: 'culture' },
    'the-tailgate':   { label: 'The Tailgate',   cardClass: 'comedy',   kickerClass: 'comedy' },
    'daily-links':    { label: 'Daily Links',    cardClass: '',         kickerClass: '' },
    'the-card':       { label: 'The Card',       cardClass: 'sponsored',kickerClass: 'partner' },
    'partner-content':{ label: 'Partner Content',cardClass: 'sponsored',kickerClass: 'partner' }
  };

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  function deskOf(a) { return DESKS[a.desk] || DESKS['news']; }

  function loadArticles() {
    return fetch('articles.json', { cache: 'no-cache' })
      .then(function (r) {
        if (!r.ok) throw new Error('articles.json failed to load (' + r.status + ')');
        return r.json();
      })
      .then(function (data) {
        var list = Array.isArray(data) ? data : (data.articles || []);
        return list.slice().sort(function (a, b) { return a.date < b.date ? 1 : -1; });
      });
  }

  function articleURL(a) { return 'article/' + encodeURIComponent(a.slug) + '.html'; }

  function cardHTML(a) {
    var d = deskOf(a);
    var cls = 'card' + (d.cardClass ? ' ' + d.cardClass : '');
    var disclosure = a.sponsored ? '<p><i>This article is a paid promotion.</i></p>' : '';
    var thumb = a.imageShare ? '<img class="thumb" src="' + esc(a.imageShare) + '" alt="" loading="lazy">' : '';
    return '<a class="' + cls + '" href="' + articleURL(a) + '">' + thumb +
      '<div class="kicker ' + d.kickerClass + '">' + esc(d.label) + '</div>' +
      '<h3>' + esc(a.title) + '</h3>' + disclosure +
      '<p>' + esc(a.excerpt) + '</p>' +
      '<div class="byline">By <b>' + esc(String(a.author).toUpperCase()) + '</b> · ' + esc(a.displayDate) + '</div></a>';
  }

  function renderInto(el, articles) {
    el.innerHTML = articles.map(cardHTML).join('');
  }

  /* ---------------- Homepage ---------------- */
  function initHome() {
    var grid = document.getElementById('latest-grid');
    if (!grid) return;
    var heroMain = document.getElementById('hero-main');
    var heroSide = document.getElementById('hero-side');
    var heading = document.getElementById('latest-heading');
    var note = document.getElementById('filter-note');
    var params = new URLSearchParams(location.search);
    var deskFilter = params.get('desk');

    loadArticles().then(function (articles) {
      if (deskFilter && DESKS[deskFilter]) {
        var filtered = articles.filter(function (a) { return a.desk === deskFilter; });
        if (heading) heading.textContent = DESKS[deskFilter].label;
        if (note) note.innerHTML = 'Showing the ' + esc(DESKS[deskFilter].label) +
          ' desk. <a href="index.html">See all articles →</a>';
        if (heroMain) heroMain.style.display = 'none';
        if (heroSide) heroSide.style.display = 'none';
        renderInto(grid, filtered.length ? filtered : articles);
        return;
      }
      // Hero = most recent article; side stack = next three; grid = the rest.
      var hero = articles[0];
      if (hero && heroMain) {
        var d = deskOf(hero);
        var heroImg = hero.image ? '<img class="hero-img" src="' + esc(hero.image) + '" alt="">' : '';
        heroMain.innerHTML =
          '<div class="kicker ' + d.kickerClass + '">The Latest · ' + esc(d.label) + '</div>' +
          heroImg +
          '<h1><a href="' + articleURL(hero) + '">' + esc(hero.title) + '</a></h1>' +
          '<p class="dek">' + esc(hero.excerpt) + '</p>' +
          '<div class="byline">By <b>' + esc(String(hero.author).toUpperCase()) + '</b> · ' +
          esc(hero.authorRole || '') + ' · ' + esc(hero.displayDate) + '</div>';
      }
      if (heroSide) {
        heroSide.innerHTML = articles.slice(1, 4).map(function (a) {
          var dd = deskOf(a);
          var sideImg = a.imageShare ? '<img class="thumb" src="' + esc(a.imageShare) + '" alt="" loading="lazy">' : '';
          return '<div class="sidecard">' + sideImg + '<div class="kicker ' + dd.kickerClass + '">' + esc(dd.label) + '</div>' +
            '<h3><a href="' + articleURL(a) + '">' + esc(a.title) + '</a></h3>' +
            '<div class="byline">By <b>' + esc(String(a.author).toUpperCase()) + '</b></div></div>';
        }).join('');
      }
      renderInto(grid, articles.slice(1));
    }).catch(function (err) {
      grid.innerHTML = '<p class="filter-note">Articles failed to load. If you opened this file directly, serve the folder with any static server (see README.md). ' + esc(err.message) + '</p>';
    });
  }

  /* ---------------- Article page ---------------- */
  function initArticle() {
    var shell = document.getElementById('article-body');
    if (!shell) return;
    var slug = new URLSearchParams(location.search).get('slug');
    loadArticles().then(function (articles) {
      var a = null;
      for (var i = 0; i < articles.length; i++) if (articles[i].slug === slug) { a = articles[i]; break; }
      if (!a) {
        shell.innerHTML = '<div class="article-body-card"><h1>Article not found</h1>' +
          '<p class="dek">That link doesn\'t match a story in our archive yet. <a href="index.html">Back to the homepage →</a></p></div>';
        document.title = 'Not found — Bills News Consolidated';
        return;
      }
      var d = deskOf(a);
      document.title = a.title + ' — Bills News Consolidated';
      var disclosure = a.sponsored
        ? '<div class="disclosure"><b>Partner Content — Paid Promotion</b>' +
          'This article is a paid promotion sponsored by a Bills News Consolidated advertiser. Sponsored columns are produced separately from our news coverage.</div>'
        : '';

      var body = '';
      (a.body || []).forEach(function (p, idx) {
        body += '<p>' + esc(p) + '</p>';
        if (idx === 1) body += '<div class="adslot inarticle-ad">Ad — In-Article (AdSense unit goes here)</div>';
      });

      var heroFig = a.image
        ? '<figure class="hero-fig"><img src="' + esc(a.image) + '" alt="">' +
          (a.imageCredit ? '<figcaption class="img-credit">' + esc(a.imageCredit) + '</figcaption>' : '') + '</figure>'
        : '';

      shell.innerHTML =
        '<article class="article-body-card">' +
          '<div class="kicker ' + d.kickerClass + '">' + esc(d.label) + '</div>' +
          '<h1>' + esc(a.title) + '</h1>' +
          '<p class="dek">' + esc(a.excerpt) + '</p>' +
          '<div class="byline">By <b>' + esc(String(a.author).toUpperCase()) + '</b> · ' +
            esc(a.authorRole || '') + ' · ' + esc(a.displayDate) + '</div>' +
          disclosure +
          heroFig +
          '<div class="article-text">' + body + '</div>' +
        '</article>';

      var related = document.getElementById('related-grid');
      if (related) {
        var rel = articles.filter(function (x) { return x.slug !== a.slug && x.desk === a.desk; })
          .concat(articles.filter(function (x) { return x.slug !== a.slug && x.desk !== a.desk; }))
          .slice(0, 3);
        renderInto(related, rel);
      }
    }).catch(function (err) {
      shell.innerHTML = '<div class="article-body-card"><h1>Couldn\'t load this article</h1><p class="dek">' + esc(err.message) + '</p></div>';
    });
  }

  /* ---------------- Writers page ---------------- */
  function initWriters() {
    var lists = document.querySelectorAll('[data-author-articles]');
    if (!lists.length) return;
    loadArticles().then(function (articles) {
      lists.forEach(function (el) {
        var name = el.getAttribute('data-author-articles');
        var mine = articles.filter(function (a) { return a.author === name; }).slice(0, 3);
        el.innerHTML = mine.length
          ? 'Latest: ' + mine.map(function (a) {
              return '<a href="' + articleURL(a) + '">' + esc(a.title) + '</a>';
            }).join(' · ')
          : 'First column files soon.';
      });
    }).catch(function () { /* leave default text in place */ });
  }

  /* ---------------- Newsletter signup forms ----------------
     Connected 2026-10-29 to Netlify Forms (form name "blitz-signup"):
     submits POST natively to Netlify, which stores the email and redirects
     to /thanks.html. Submissions live in the Netlify dashboard (Forms tab)
     and can be exported to MailerLite later. Do NOT intercept submits here —
     that was the old demo behavior that silently discarded signups. */
  function initSignupForms() { /* Netlify Forms handles submits natively. */ }

  document.addEventListener('DOMContentLoaded', function () {
    initHome();
    initArticle();
    initWriters();
    initSignupForms();
  });
})();
