// Cyberflix frontend interactions

document.addEventListener('click', function (e) {
  const t = e.target;
  if (t.matches('.pw-toggle')) {
    const targetId = t.getAttribute('data-target');
    const input = document.getElementById(targetId);
    if (!input) return;
    if (input.type === 'password') {
      input.type = 'text';
      t.textContent = 'Hide';
    } else {
      input.type = 'password';
      t.textContent = 'Show';
    }
  }
});

// Enhance submit buttons with a loading state
document.addEventListener('submit', function (e) {
  const btn = e.target.querySelector('button[type=submit]');
  if (btn) {
    btn.disabled = true;
    const old = btn.textContent;
    btn.textContent = 'Please wait...';
    setTimeout(() => { btn.textContent = old; btn.disabled = false; }, 3000);
  }
});
