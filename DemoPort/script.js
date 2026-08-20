const menuToggle = document.querySelector('.menu-toggle');
const mainNav = document.querySelector('#main-nav');
const filters = document.querySelectorAll('.filter');
const projects = document.querySelectorAll('.project-card');
const copyButton = document.querySelector('#copy-email');
const toast = document.querySelector('#toast');

menuToggle.addEventListener('click', () => {
  const isOpen = mainNav.classList.toggle('open');
  menuToggle.setAttribute('aria-expanded', String(isOpen));
  menuToggle.textContent = isOpen ? '닫기' : '메뉴';
});

document.querySelectorAll('.main-nav a').forEach((link) => {
  link.addEventListener('click', () => {
    mainNav.classList.remove('open');
    menuToggle.setAttribute('aria-expanded', 'false');
    menuToggle.textContent = '메뉴';
  });
});

filters.forEach((filter) => {
  filter.addEventListener('click', () => {
    filters.forEach((item) => item.classList.remove('active'));
    filter.classList.add('active');
    const selectedCategory = filter.dataset.filter;
    projects.forEach((project) => {
      project.classList.toggle('hidden', selectedCategory !== 'all' && project.dataset.category !== selectedCategory);
    });
  });
});

copyButton.addEventListener('click', async () => {
  try {
    await navigator.clipboard.writeText('goukim79@gmail.com');
    toast.classList.add('show');
    window.setTimeout(() => toast.classList.remove('show'), 2200);
  } catch {
    window.location.href = 'mailto:goukim79@gmail.com';
  }
});
