/* BNC Blitz conversion layer for article pages (added 2026-11-02, owner's pick:
   scroll pop-up + soft gate). Behavior:
   - At 40% scroll, show the MailerLite Blitz pop-up form (q2woz5) once;
     after a showing, stay quiet for 7 days (localStorage timestamp).
   - Film Room email-gate TEST (2026-11-23 → 2026-12-07): Film Room articles
     hide everything past the first ~35% behind a Blitz signup card (no skip
     button). "Join free" opens the same pop-up and unlocks the article;
     joining sets the joined flag, which unlocks every Film Room gate for
     returning readers. All other desks are ungated. Content is never
     removed from the HTML — this is a soft gate only, so shares/SEO are
     unaffected. */
(function () {
  var JOINED = 'bncBlitzJoined';
  var POPUP_AT = 'bncPopupShownAt';
  var GATE_AT = 'bncGatePassedAt';
  var DAY = 24 * 3600 * 1000;

  function get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function fresh(k, days) {
    var t = parseInt(get(k) || '0', 10);
    return t > 0 && (Date.now() - t) < days * DAY;
  }
  function joined() { return get(JOINED) === '1'; }
  function gatePassed() { return joined() || fresh(GATE_AT, 30); }

  function unlockGate() {
    var t = document.getElementById('gateTail');
    if (t) { t.classList.add('open'); }
    var c = document.getElementById('gateCta');
    if (c) { c.style.display = 'none'; }
  }

  window.bncJoin = function () {
    set(JOINED, '1');
    unlockGate();
    if (window.ml) { ml('show', 'q2woz5', true); }
  };
  window.bncKeepReading = function () {
    set(GATE_AT, String(Date.now()));
    unlockGate();
  };

  // Film Room test gate: only an actual join unlocks it for returning
  // readers (there is no skip pass on that card). Other gates keep the
  // legacy joined-or-recently-passed behavior.
  var isFrGate = !!document.querySelector('.gate-wrap.fr');
  if (isFrGate ? joined() : gatePassed()) { unlockGate(); }

  var shown = false;
  function onScroll() {
    if (shown || joined() || fresh(POPUP_AT, 7)) { return; }
    var h = document.documentElement;
    var max = h.scrollHeight - h.clientHeight;
    if (max <= 0) { return; }
    if (h.scrollTop / max >= 0.4) {
      shown = true;
      set(POPUP_AT, String(Date.now()));
      window.removeEventListener('scroll', onScroll);
      if (window.ml) { ml('show', 'q2woz5', true); }
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
})();
