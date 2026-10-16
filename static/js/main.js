document.addEventListener('click', function (e) {
  const toggleButton = e.target.closest('.pw-toggle');
  if (!toggleButton) return;

  const targetId = toggleButton.getAttribute('data-target');
  const input = document.getElementById(targetId);
  if (!input) return;

  if (input.type === 'password') {
    input.type = 'text';
    toggleButton.textContent = 'Hide';
  } else {
    input.type = 'password';
    toggleButton.textContent = 'Show';
  }
});

document.addEventListener('submit', function (e) {
  const button = e.target.querySelector('button[type="submit"]');
  if (!button) return;

  button.disabled = true;
  const originalText = button.textContent;
  button.textContent = 'Please wait...';

  setTimeout(() => {
    button.disabled = false;
    button.textContent = originalText;
  }, 3000);
});
