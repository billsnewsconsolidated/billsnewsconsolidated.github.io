/* BNC Blitz conversion layer for article pages (added 2026-11-02, owner's pick:
   scroll pop-up + soft gate). Behavior:
   - At 40% scroll, show the MailerLite Blitz pop-up form (q2woz5) once;
     after a showing, stay quiet for 7 days (localStorage timestamp).
   - The final section of each article renders faded behind a signup card.
     "Join free" opens the same pop-up and unlocks the ending; "Keep reading"
     unlocks too and suppresses the gate for 30 days. Joining (clicking any
     Join button) suppresses both the gate and the pop-up permanently-ish
     (joined flag). Content is never removed from the HTML — this is a soft
     gate only, so shares/SEO are unaffected. */
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

  if (gatePassed()) { unlockGate(); }

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
