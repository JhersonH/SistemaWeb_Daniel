document.addEventListener('DOMContentLoaded', function () {
  const toggleBtn = document.getElementById('toggleSidebar');
  const container = document.getElementById('dashboardContainer');

  if (toggleBtn && container) {
    toggleBtn.addEventListener('click', () => {
      container.classList.toggle('collapsed');
    });
  }
});
