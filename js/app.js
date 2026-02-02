const button = document.getElementById('actionBtn');
const status = document.getElementById('status');

button.addEventListener('click', () => {
  status.textContent = 'Clicked! You can start building here.';
});
