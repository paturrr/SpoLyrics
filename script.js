// Tourrr Agent — SpoLyrics landing page interactivity

// ===== 1) i18n (EN default, ID optional) =====
const translations = {
  en: {}, // English is the default text already in the HTML
  id: {
    nav_demo: 'Demo Langsung',
    nav_features: 'Fitur',
    nav_controls: 'Kontrol',
    nav_install: 'Instalasi',
    nav_cta: 'Pasang Sekarang',
    hero_title: 'Lirik Spotify <span class="grad">Tanpa Delay.</span><br />Tanpa Ribet.',
    hero_sub:
      'SpoLyrics adalah miniplayer lirik Spotify yang <strong>minimalis</strong>, <strong>transparan</strong>, dan <strong>sinkron presisi 100%</strong> menggunakan Windows System Media Transport Controls. Dibangun dengan Python untuk pengalaman mendengarkan yang lebih baik saat kamu bekerja.',
    hero_cta_primary: 'Mulai Instalasi',
    hero_cta_ghost: 'Lihat Fitur ▾',
    stat_version: 'Versi Terbaru',
    stat_features: 'Fitur',
    stat_sync: 'Sinkron Presisi',
    stat_supported: 'Didukung',
    stat_license: 'Lisensi',
    stat_exclusive: 'Eksklusif',
    about_title: 'Tentang Aplikasi',
    about_p1:
      'SpoLyrics dibuat untuk menjawab keluhan sederhana dari teman-teman: mereka ingin mendengarkan lagu di Spotify atau YouTube Music sambil bekerja, tapi miniplayer resmi tidak menampilkan lirik apa pun.',
    about_p2:
      'Aplikasi ini mengambil data durasi secara <strong>real-time langsung dari inti sistem Windows</strong>, sehingga sinkronisasi lirik presisi 100% tanpa bergantung pada server pihak ketiga. Hasilnya: lirik mengalir bersama lagu, sehalus mungkin.',
    about_p3:
      '<svg class="ico" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M12 2a7 7 0 0 0-4 12.7c.6.5 1 1.3 1 2.3h6c0-1 .4-1.8 1-2.3A7 7 0 0 0 12 2z"/></svg> SpoLyrics masih dalam pengembangan aktif. Temukan bug atau punya ide? Jangan ragu buka issue di GitHub!',
    features_eyebrow: 'Kenapa SpoLyrics?',
    demo_eyebrow: 'Coba Sekarang',
    demo_title: 'Demo Langsung',
    demo_sub: 'Penasaran gimana rasanya? Mainkan simulasi interaktif di bawah — tanpa perlu instal.',
    demo_hint: 'Ini simulasi visual dari aplikasi desktop. Aplikasi asli sinkron langsung dengan Spotify milikmu.',
    features_title: 'Fitur Unggulan',
    features_sub: 'Dirancang ramping, cepat, dan elegan — hanya yang kamu butuhkan.',
    feat1_t: 'Zero-Delay Sync',
    feat1_d: 'Sinkronisasi waktu 100% presisi. Mengambil data durasi real-time langsung dari inti OS Windows.',
    feat2_t: 'Smart Duration Match',
    feat2_d: 'Menyocokkan lirik otomatis berdasarkan durasi versi lagu yang diputar — beresin mismatch Radio Edit vs Album Version.',
    feat3_t: 'Glassmorphism UI',
    feat3_d: 'Desain elegan, transparan, dan tanpa border. Menyatu indah dengan wallpaper desktop-mu.',
    feat4_t: 'Freely Draggable',
    feat4_d: 'Klik kiri tahan di mana saja untuk menyeret jendela lirik ke posisi favoritmu.',
    feat5_t: 'System Tray Integration',
    feat5_d: 'Berjalan senyap di background. Klik kanan ikon tray untuk buka pengaturan, sembunyikan lirik, atau lihat shortcut.',
    feat6_t: 'Advanced Customization',
    feat6_d: 'Ganti warna lirik (color picker HSV real-time), atur transparansi, dan aktifkan "Auto-Start with Windows". Tersimpan permanen.',
    feat7_t: 'Auto Update Checker',
    feat7_d: 'Otomatis mengecek versi terbaru dari PyPI dan menawarkan pengalaman update 1-klik yang mulus.',
    feat8_t: 'Smart Scroll Cooldown',
    feat8_d: 'Mencegah ketidaksengajaan melompati banyak lagu sekaligus dengan jeda 800ms saat men-scroll lagu dengan roda mouse.',
    controls_eyebrow: 'Rahasia Kecil',
    controls_title: 'Kontrol Tak Terlihat',
    controls_sub: 'UI super bersih tanpa tombol konvensional. Gunakan gestur mouse ini:',
    ctrl1: 'Play / Pause',
    ctrl2: 'Next / Previous track',
    ctrl3: 'Toggle Pin / Lock jendela <svg class="ico" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>',
    ctrl4: 'Toggle judul lagu',
    ctrl5: 'Perbesar / perkecil font',
    ctrl6: 'Ubah ukuran jendela',
    ctrl7: 'Tutup aplikasi',
    ctrl8: 'Middle click (touchpad)',
    install_eyebrow: 'Mulai',
    install_title: 'Cara Instalasi',
    install_sub: 'Satu perintah. Butuh Python 3.8 – 3.12 (jangan pakai 3.13!)',
    install_pip_t: '<svg class="ico" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 13c-1.5 1.5-2 5-2 5s3.5-.5 5-2"/><path d="M12 15l-3-3a14 14 0 0 1 7-9c2 0 3 1 3 3a14 14 0 0 1-9 7z"/><circle cx="14.5" cy="9.5" r="1"/></svg> Instal via pip',
    install_pip_d: 'Buka Windows Terminal / Command Prompt lalu jalankan:',
    install_pip_note: 'Kalau muncul error <code>pip is not recognized</code>, pakai <code>python -m pip install spolyrics</code>.',
    install_run_t: '<svg class="ico" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="6 4 20 12 6 20 6 4"/></svg> How to Run',
    install_run_d: 'Setelah terpasang, jalankan dari direktori mana pun:',
    install_run_note: 'Atau tanpa terminal hitam: <code>pythonw -m main</code>. Pastikan Spotify sedang memutar lagu! <svg class="ico" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>',
    install_os_note:
      '<strong class="warn-strong"><svg class="ico" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg> Penting — Dukungan OS:</strong> SpoLyrics <strong>eksklusif untuk Windows</strong> (10/11). Karena memakai <code>winsdk</code> untuk performa 0-delay tanpa server pihak ketiga, aplikasi ini <strong>tidak bisa</strong> diinstal di macOS atau Linux.',
    update_label: 'Update ke versi terbaru:',
    uninstall_label: 'Hapus:',
    cta_title: 'Siap menyanyi bersama lagumu? <svg class="ico" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>',
    cta_sub: 'Pasang SpoLyrics sekarang dan nikmati lirik yang mengalir sempurna dengan musikmu.',
    cta_primary: 'Pasang Sekarang',
    cta_ghost: 'Lihat di GitHub',
    footer_tagline: 'Miniplayer lirik Spotify transparan & tanpa delay untuk Windows.',
    footer_report: 'Lapor Issue',
    footer_top: 'Kembali ke Atas ↑',
    footer_license: 'Lisensi MIT',
    copy_btn: 'Copy',
  },
};

// Cache the original English strings so switching back to EN is lossless
const enCache = {};
document.querySelectorAll('[data-i18n]').forEach((el) => {
  enCache[el.getAttribute('data-i18n')] = el.textContent;
});
document.querySelectorAll('[data-i18n-html]').forEach((el) => {
  enCache[el.getAttribute('data-i18n-html')] = el.innerHTML;
});

function applyLanguage(lang) {
  const dict = lang === 'id' ? translations.id : null;
  // text nodes
  document.querySelectorAll('[data-i18n]').forEach((el) => {
    const key = el.getAttribute('data-i18n');
    const val = dict ? dict[key] : enCache[key];
    if (val != null) el.textContent = val;
  });
  // html nodes (contain inline tags)
  document.querySelectorAll('[data-i18n-html]').forEach((el) => {
    const key = el.getAttribute('data-i18n-html');
    const val = dict ? dict[key] : enCache[key];
    if (val != null) el.innerHTML = val;
  });
  document.documentElement.lang = lang;
  // update button states
  document.querySelectorAll('.lang-btn').forEach((btn) => {
    const active = btn.getAttribute('data-lang') === lang;
    btn.classList.toggle('active', active);
    btn.setAttribute('aria-pressed', active ? 'true' : 'false');
  });
  try {
    localStorage.setItem('spolyrics_lang', lang);
  } catch (e) {}
}

// wire up buttons
document.querySelectorAll('.lang-btn').forEach((btn) => {
  btn.addEventListener('click', () => applyLanguage(btn.getAttribute('data-lang')));
});

// init: default English, but respect a previously chosen language
let savedLang = 'en';
try {
  savedLang = localStorage.getItem('spolyrics_lang') || 'en';
} catch (e) {}
applyLanguage(savedLang);

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

  render(); // initial paint
  play(); // auto-start demo on page load
})();
