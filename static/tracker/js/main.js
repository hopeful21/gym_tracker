(() => {
  document.querySelectorAll('img[data-fallback]').forEach((image) => { image.addEventListener('error', () => { if (image.src !== image.dataset.fallback) { image.src = image.dataset.fallback; image.alt = image.dataset.fallbackAlt || 'Fitness visual reference'; } }, { once: true }); });
  const clock = document.querySelector('[data-clock]');
  if (clock) { const updateClock = () => { clock.textContent = new Intl.DateTimeFormat(undefined, {hour:'2-digit', minute:'2-digit'}).format(new Date()); }; updateClock(); window.setInterval(updateClock, 30000); }
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#main-nav');
  toggle?.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', String(!open));
    nav.classList.toggle('nav-open', !open);
  });
  document.querySelectorAll('[data-live-timer]').forEach((timer) => {
    const started = Date.parse(timer.dataset.start);
    const paused = Number(timer.dataset.paused || 0);
    const pausedAt = timer.dataset.pausedAt ? Date.parse(timer.dataset.pausedAt) : null;
    const status = timer.dataset.status;
    const update = () => {
      const end = status === 'paused' && pausedAt ? pausedAt : Date.now();
      const seconds = Math.max(0, Math.floor((end - started) / 1000) - paused);
      const h = String(Math.floor(seconds / 3600)).padStart(2, '0');
      const m = String(Math.floor((seconds % 3600) / 60)).padStart(2, '0');
      const s = String(seconds % 60).padStart(2, '0');
      timer.textContent = `${h}:${m}:${s}`;
    };
    update();
    if (status === 'active') window.setInterval(update, 1000);
  });
  const panel = document.querySelector('[data-rest-timer]');
  if (!panel) return;
  const defaultSeconds = Number(panel.dataset.defaultSeconds || 60);
  const display = panel.querySelector('[data-rest-display]');
  const startButton = panel.querySelector('[data-rest-start]');
  const soundButton = panel.querySelector('[data-sound-toggle]');
  const alarm = new Audio(panel.dataset.soundUrl);
  alarm.preload = 'auto';
  let remaining = Number(localStorage.getItem('formRestRemaining') || defaultSeconds);
  let selected = Number(localStorage.getItem('formRestPreset') || defaultSeconds);
  let deadline = null;
  let interval = null;
  let sound = localStorage.getItem('formRestSound') !== 'false';

  const render = () => {
    const min = String(Math.floor(remaining / 60)).padStart(2, '0');
    const sec = String(remaining % 60).padStart(2, '0');
    display.textContent = `${min}:${sec}`;
  };
  const finishTimer = () => {
    clearInterval(interval);
    interval = null;
    deadline = null;
    remaining = 0;
    localStorage.setItem('formRestRemaining', '0');
    localStorage.removeItem('formRestDeadline');
    startButton.textContent = 'Start';
    render();
    if (sound) {
      alarm.currentTime = 0;
      alarm.play().catch(() => {});
    }
  };
  const tick = () => {
    remaining = Math.max(0, Math.ceil((deadline - Date.now()) / 1000));
    localStorage.setItem('formRestRemaining', String(remaining));
    render();
    if (remaining <= 0) finishTimer();
  };

  const savedDeadline = Number(localStorage.getItem('formRestDeadline') || 0);
  if (savedDeadline > Date.now()) {
    deadline = savedDeadline;
    remaining = Math.ceil((deadline - Date.now()) / 1000);
    startButton.textContent = 'Pause';
    interval = window.setInterval(tick, 250);
  } else if (savedDeadline) {
    localStorage.removeItem('formRestDeadline');
  }

  panel.querySelectorAll('[data-rest-seconds]').forEach((button) => {
    button.classList.toggle('selected', Number(button.dataset.restSeconds) === selected);
    button.addEventListener('click', () => {
      clearInterval(interval);
      interval = null;
      deadline = null;
      startButton.textContent = 'Start';
      localStorage.removeItem('formRestDeadline');
      selected = Number(button.dataset.restSeconds);
      remaining = selected;
      localStorage.setItem('formRestPreset', String(selected));
      localStorage.setItem('formRestRemaining', String(remaining));
      panel.querySelectorAll('[data-rest-seconds]').forEach((preset) => preset.classList.toggle('selected', preset === button));
      render();
    });
  });

  startButton.addEventListener('click', () => {
    if (interval) {
      clearInterval(interval);
      interval = null;
      deadline = null;
      localStorage.removeItem('formRestDeadline');
      startButton.textContent = 'Resume';
      return;
    }
    if (remaining <= 0) remaining = selected;
    deadline = Date.now() + remaining * 1000;
    localStorage.setItem('formRestDeadline', String(deadline));
    interval = window.setInterval(tick, 250);
    startButton.textContent = 'Pause';
  });

  panel.querySelector('[data-rest-dismiss]').addEventListener('click', () => {
    clearInterval(interval);
    localStorage.removeItem('formRestDeadline');
    localStorage.removeItem('formRestRemaining');
    panel.hidden = true;
  });
  panel.querySelector('[data-rest-reset]').addEventListener('click', () => {
    clearInterval(interval);
    interval = null;
    deadline = null;
    localStorage.removeItem('formRestDeadline');
    remaining = selected;
    localStorage.setItem('formRestRemaining', String(remaining));
    startButton.textContent = 'Start';
    render();
  });
  soundButton.setAttribute('aria-pressed', String(sound));
  soundButton.textContent = sound ? '◖ Sound on' : '◖ Sound off';
  soundButton.addEventListener('click', () => {
    sound = !sound;
    localStorage.setItem('formRestSound', String(sound));
    soundButton.setAttribute('aria-pressed', String(sound));
    soundButton.textContent = sound ? '◖ Sound on' : '◖ Sound off';
    if (sound) alarm.load();
  });
  render();
})();
