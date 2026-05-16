document.addEventListener('DOMContentLoaded', () => {
  // Theme Management
  const themeToggle = document.getElementById('theme-toggle');
  const body = document.body;
  
  // Check local storage or OS preference
  const savedTheme = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  
  if (savedTheme) {
    body.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
  } else if (prefersDark) {
    body.setAttribute('data-theme', 'dark');
    updateThemeIcon('dark');
  }
  
  themeToggle.addEventListener('click', () => {
    const currentTheme = body.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    body.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
  });
  
  function updateThemeIcon(theme) {
    // Simple text replacement for MVP, can use SVGs later
    themeToggle.textContent = theme === 'dark' ? '☀️' : '🌙';
  }
});
