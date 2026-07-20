// Tourrr Agent — SpoLyrics landing page interactivity

// ===== 1) i18n (EN default, ID optional) =====
const translations = {
  en: {}, // English is the default text already in the HTML
  id: {
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
    stat_supported: 'Didukung',
    stat_license: 'Lisensi',
    stat_exclusive: 'Eksklusif',
    about_title: 'Tentang Aplikasi',
    about_p1:
      'SpoLyrics dibuat untuk menjawab keluhan sederhana dari teman-teman: mereka ingin mendengarkan lagu di Spotify atau YouTube Music sambil bekerja, tapi miniplayer resmi tidak menampilkan lirik apa pun.',
    about_p2:
      'Aplikasi ini mengambil data durasi secara <strong>real-time langsung dari inti sistem Windows</strong>, sehingga sinkronisasi lirik presisi 100% tanpa bergantung pada server pihak ketiga. Hasilnya: lirik mengalir bersama lagu, sehalus mungkin.',
    about_p3:
      '💡 SpoLyrics masih dalam pengembangan aktif. Temukan bug atau punya ide? Jangan ragu buka issue di GitHub!',
    features_eyebrow: 'Kenapa SpoLyrics?',
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
    ctrl3: 'Toggle Pin / Lock jendela 🔒',
    ctrl4: 'Toggle judul lagu',
    ctrl5: 'Perbesar / perkecil font',
    ctrl6: 'Ubah ukuran jendela',
    ctrl7: 'Tutup aplikasi',
    ctrl8: 'Middle click (touchpad)',
    install_eyebrow: 'Mulai',
    install_title: 'Cara Instalasi',
    install_sub: 'Satu perintah. Butuh Python 3.8 – 3.12 (jangan pakai 3.13!)',
    install_pip_t: '🚀 Instal via pip',
    install_pip_d: 'Buka Windows Terminal / Command Prompt lalu jalankan:',
    install_pip_note: 'Kalau muncul error <code>pip is not recognized</code>, pakai <code>python -m pip install spolyrics</code>.',
    install_run_t: '▶️ Cara Menjalankan',
    install_run_d: 'Setelah terpasang, jalankan dari direktori mana pun:',
    install_run_note: 'Atau tanpa terminal hitam: <code>pythonw -m main</code>. Pastikan Spotify sedang memutar lagu! 🎵',
    install_os_note:
      '<strong>⚠️ Penting — Dukungan OS:</strong> SpoLyrics <strong>eksklusif untuk Windows</strong> (10/11). Karena memakai <code>winsdk</code> untuk performa 0-delay tanpa server pihak ketiga, aplikasi ini <strong>tidak bisa</strong> diinstal di macOS atau Linux.',
    update_label: 'Update ke versi terbaru:',
    uninstall_label: 'Hapus:',
    cta_title: 'Siap menyanyi bersama lagumu? 🎶',
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

// ===== 2) Reveal-on-scroll for sections & cards =====
const revealTargets = document.querySelectorAll(
  '.about-card, .card, .ctrl, .install-card, .note, .controls-shot, .hero-shot, .cta-card'
);
revealTargets.forEach((el) => el.classList.add('reveal'));

const io = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        io.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.12 }
);
revealTargets.forEach((el) => io.observe(el));

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
    const res = await fetch('https://pypi.org/pypi/spolyrics/json');
    const data = await res.json();
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
