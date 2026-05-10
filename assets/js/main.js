(function () {
  const LANG_KEY = 'jackpoker_lang';

  function getLang() {
    const v = localStorage.getItem(LANG_KEY);
    return v === 'ru' ? 'ru' : 'en';
  }

  function setLang(code) {
    const lang = code === 'ru' ? 'ru' : 'en';
    localStorage.setItem(LANG_KEY, lang);
    applyLang();
  }

  function applyLang() {
    const lang = getLang();
    document.documentElement.lang = lang;
    document.querySelectorAll('.lang-btn').forEach(function (b) {
      const on = b.getAttribute('data-lang') === lang;
      b.classList.toggle('active', on);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    document.querySelectorAll('.lang-en').forEach(function (el) {
      el.hidden = lang !== 'en';
    });
    document.querySelectorAll('.lang-ru').forEach(function (el) {
      el.hidden = lang !== 'ru';
    });
  }

  document.querySelectorAll('.lang-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      setLang(btn.getAttribute('data-lang'));
    });
  });
  applyLang();

  document.querySelectorAll('.faq-q').forEach(function (btn) {
    btn.addEventListener('click', function () {
      btn.closest('.faq-item').classList.toggle('open');
    });
  });

  var burger = document.querySelector('.burger');
  var wrap = document.querySelector('.nav-wrap');
  if (burger && wrap) {
    burger.addEventListener('click', function () {
      wrap.classList.toggle('open');
    });
  }
})();
