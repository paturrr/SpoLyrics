// Tourrr Agent — SpoLyrics landing page interactivity

// ===== 1) i18n (EN/ID loaded from JSON) =====
let translations = { en: {}, id: {} };

async function applyLanguage(lang) {
  const dict = translations[lang];
  if (!dict || Object.keys(dict).length === 0) {
    console.error(`Translations for '${lang}' not loaded or empty.`);
    return;
  }

  document.querySelectorAll('[data-i18n]').forEach((el) => {
    const key = el.getAttribute('data-i18n');
    if (dict[key]) el.textContent = dict[key];
  });

  document.querySelectorAll('[data-i18n-html]').forEach((el) => {
    const key = el.getAttribute('data-i18n-html');
    if (dict[key]) el.innerHTML = dict[key];
  });

  document.documentElement.lang = lang;
  document.querySelectorAll('.lang-btn').forEach((btn) => {
    const active = btn.getAttribute('data-lang') === lang;
    btn.classList.toggle('active', active);
    btn.setAttribute('aria-pressed', active ? 'true' : 'false');
  });

  try {
    localStorage.setItem('spolyrics_lang', lang);
  } catch (e) {
    console.error("Failed to save language preference:", e);
  }
}

async function initI18n() {
  try {
    const [enRes, idRes] = await Promise.all([
      fetch('lang/en.json'),
      fetch('lang/id.json')
    ]);
    translations.en = await enRes.json();
    translations.id = await idRes.json();
  } catch (e) {
    console.error("Failed to load translation files:", e);
    // Fallback or error display could be implemented here
    return;
  }

  document.querySelectorAll('.lang-btn').forEach((btn) => {
    btn.addEventListener('click', () => applyLanguage(btn.getAttribute('data-lang')));
  });
  
  let savedLang = 'en';
  try {
    savedLang = localStorage.getItem('spolyrics_lang') || 'en';
  } catch (e) {}

  applyLanguage(savedLang);
}

initI18n();

// ===== 2) AOS handles reveal-on-scroll. Count-up for hero stats =====
function animateCountUp(el, target, suffix) {
  const dur = 1400;
  const start = performance.now();
  function tick(now) {
    const p = Math.min(1, (now - start) / dur);
    const eased = 1 - Math.pow(1 - p, 3);
    el.textContent = Math.round(eased * target) + (suffix || '');
    if (p < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}
// trigger count-up when hero stats are in view
const statsObs = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.querySelectorAll('.stat-num[data-count]').forEach((s) => {
        animateCountUp(s, parseInt(s.getAttribute('data-count'), 10), s.getAttribute('data-suffix') || '');
      });
      statsObs.unobserve(entry.target);
    }
  });
}, { threshold: 0.3 });
const heroStats = document.querySelector('.hero-stats');
if (heroStats) statsObs.observe(heroStats);

// ===== 3) Copy-to-clipboard for code blocks =====
const copyLabel = () => (document.documentElement.lang === 'id' ? 'Disalin!' : 'Copied!');
document.querySelectorAll('.copy-btn').forEach((btn) => {
  btn.addEventListener('click', async () => {
    const text = btn.getAttribute('data-copy');
    const restore = () => applyLanguage(document.documentElement.lang);
    try {
      await navigator.clipboard.writeText(text);
    } catch (e) {
      const ta = document.createElement('textarea');
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
    }
    btn.textContent = copyLabel();
    btn.classList.add('copied');
    setTimeout(() => {
      btn.classList.remove('copied');
      restore();
    }, 1400);
  });
});

// ===== 4) Subtle navbar shadow on scroll =====
const navbar = document.querySelector('.navbar');
window.addEventListener('scroll', () => {
  if (window.scrollY > 40) navbar.style.boxShadow = '0 8px 32px rgba(0,0,0,0.6)';
  else navbar.style.boxShadow = '';
});

// ===== 5) Auto-fetch latest version from PyPI =====
async function fetchLatestVersion() {
  try {
    const response = await fetch(`https://pypi.org/pypi/spolyrics/json?t=${new Date().getTime()}`);
    const data = await response.json();
    if (data && data.info && data.info.version) {
      const versionEl = document.getElementById('live-version');
      if (versionEl) {
        versionEl.textContent = data.info.version;
      }
    }
  } catch (e) {
    console.error('Failed to fetch version from PyPI', e);
  }
}
fetchLatestVersion();

// ===== 6) Interactive Demo Player (visual simulation) =====
(function () {
  const demoSongs = [
    {
      artist: 'Aurora',
      song: 'Runaway',
      lines: [
        { t: 0,  c: 'I was listening to the ocean' },
        { t: 3,  c: 'Saw a face in the sand' },
        { t: 6,  c: 'But when I picked it up' },
        { t: 9,  c: 'Then it vanished away' },
        { t: 12, c: 'And when I looked up' },
        { t: 15, c: 'It felt like a story' },
        { t: 18, c: "And I said 'Take me home'" },
        { t: 22, c: 'And take me all the way' },
      ],
    },
    {
      artist: 'Lauv',
      song: 'I Like Me Better',
      lines: [
        { t: 0,  c: "I don't know what it is" },
        { t: 3,  c: "But I got that feeling" },
        { t: 6,  c: "Waking up in this bed next to you" },
        { t: 9,  c: "Swear the room, yeah, it got no ceiling" },
        { t: 13, c: "I like me better when I'm with you" },
        { t: 17, c: "I like me better when I'm with you" },
        { t: 21, c: "I knew from the first time" },
        { t: 24, c: "I'd stay for a long time" },
      ],
    },
    {
      artist: 'Coldplay',
      song: 'Yellow',
      lines: [
        { t: 0,  c: 'Look at the stars' },
        { t: 3,  c: 'Look how they shine for you' },
        { t: 7,  c: 'And everything you do' },
        { t: 10, c: 'Yeah, they were all yellow' },
        { t: 14, c: 'I came along' },
        { t: 17, c: 'I wrote a song for you' },
        { t: 20, c: 'And all the things you do' },
        { t: 24, c: 'And it was called yellow' },
      ],
    },
  ];

  const el = {
    player: document.getElementById('demoPlayer'),
    title: document.getElementById('dpTitle'),
    current: document.getElementById('dpCurrent'),
    next: document.getElementById('dpNext'),
    fill: document.getElementById('dpFill'),
    play: document.getElementById('dcPlay'),
    prev: document.getElementById('dcPrev'),
    nextBtn: document.getElementById('dcNext'),
    song: document.getElementById('dcSong'),
  };
  if (!el.player) return; // demo section not present

  let idx = 0;
  let elapsed = 0;
  let timer = null;
  let playing = false;
  const TICK = 100; // ms
  const songDuration = (s) => s.lines[s.lines.length - 1].t + 4;

  function render() {
    const song = demoSongs[idx];
    const dur = songDuration(song);
    el.title.innerHTML = '<svg class="dp-note" viewBox="0 0 24 24" width="12" height="12" fill="currentColor" aria-hidden="true"><path d="M12 3v10.55A4 4 0 1 0 14 17V7h4V3h-6z"/></svg>' +
      '<span class="dp-song-name">' + song.song + '</span>' +
      '<span class="dp-dot">•</span>' +
      '<span class="dp-artist">' + song.artist + '</span>';
    el.song.textContent = `Demo Track ${idx + 1} / ${demoSongs.length}`;

    // find current line
    let curLine = song.lines[0];
    let nextLine = null;
    for (let i = 0; i < song.lines.length; i++) {
      if (elapsed >= song.lines[i].t) {
        curLine = song.lines[i];
        nextLine = song.lines[i + 1] || null;
      }
    }
    el.current.textContent = curLine.c;
    el.next.textContent = nextLine ? nextLine.c : '';
    el.fill.style.width = Math.min(100, (elapsed / dur) * 100) + '%';
  }

  function tick() {
    elapsed += TICK / 1000;
    const dur = songDuration(demoSongs[idx]);
    if (elapsed >= dur) {
      // auto-advance to next song
      idx = (idx + 1) % demoSongs.length;
      elapsed = 0;
    }
    render();
  }

  function setPlayIcon(isPlaying) {
    const p = el.play.querySelector('.ic-play');
    const q = el.play.querySelector('.ic-pause');
    if (p) p.style.display = isPlaying ? 'none' : 'block';
    if (q) q.style.display = isPlaying ? 'block' : 'none';
  }

  function play() {
    if (playing) return;
    playing = true;
    setPlayIcon(true);
    timer = setInterval(tick, TICK);
  }
  function pause() {
    playing = false;
    setPlayIcon(false);
    if (timer) clearInterval(timer);
    timer = null;
  }
  function togglePlay() { playing ? pause() : play(); }
  function goto(newIdx) {
    idx = (newIdx + demoSongs.length) % demoSongs.length;
    elapsed = 0;
    render();
  }

  el.play.addEventListener('click', togglePlay);
  el.nextBtn.addEventListener('click', () => goto(idx + 1));
  el.prev.addEventListener('click', () => goto(idx - 1));

  // FAQ single-open accordion
  document.querySelectorAll('.faq-item').forEach(item => {
    item.addEventListener('toggle', () => {
      if (item.open) {
        document.querySelectorAll('.faq-item').forEach(other => {
          if (other !== item && other.open) other.open = false;
        });
      }
    });
  });

  render(); // initial paint
  play(); // auto-start demo on page load
})();
