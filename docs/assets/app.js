document.addEventListener('DOMContentLoaded', () => {
  const s = document.getElementById('search');
  const grid = document.getElementById('grid');
  if(!s || !grid) return;
  s.addEventListener('input', () => {
    const q = s.value.trim().toLowerCase();
    [...grid.children].forEach(card => {
      const text = card.textContent.toLowerCase();
      card.style.display = text.includes(q) ? '' : 'none';
    });
  });
});
