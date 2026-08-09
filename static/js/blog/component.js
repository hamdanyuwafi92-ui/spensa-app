// function initNavbar() {
//     const header = document.querySelector('header');
//     if (!header) return;
//     window.addEventListener('scroll', () => {
//         header.classList.toggle('scrolled', window.scrollY > BLOG_CONFIG.scrollOffset);
//     });
// }

// function initMobileMenu() {
//     const mobileBtn = document.querySelector('.mobile-toggle');
//     const navLinks = document.querySelector('.nav-links');
//     if (!mobileBtn || !navLinks) return;

//     mobileBtn.addEventListener('click', function (e) {
//         e.stopPropagation();
//         if (navLinks.classList.contains('show')) {
//             navLinks.classList.remove('show');
//             mobileBtn.innerHTML = '<i class="fa-solid fa-bars-staggered"></i>';
//         } else {
//             navLinks.classList.add('show');
//             mobileBtn.innerHTML = '<i class="fa-solid fa-xmark"></i>';
//         }
//     });

//     document.addEventListener('click', function (e) {
//         if (!navLinks.contains(e.target) && !mobileBtn.contains(e.target)) {
//             navLinks.classList.remove('show');
//             mobileBtn.innerHTML = '<i class="fa-solid fa-bars-staggered"></i>';
//         }
//     });
// }

// function initLightbox() {
//     const lightbox = document.querySelector('.lightbox');
//     if (!lightbox) return;

//     const lightboxImg = lightbox.querySelector('.lightbox-content');
//     const closeBtn = lightbox.querySelector('.lightbox-close');

//     document.querySelectorAll('.photo-item').forEach(item => {
//         item.addEventListener('click', () => {
//             const img = item.querySelector('img');
//             if (img) {
//                 lightboxImg.src = img.src;
//                 lightbox.classList.add('active');
//             }
//         });
//     });

//     if (closeBtn) {
//         closeBtn.addEventListener('click', () => lightbox.classList.remove('active'));
//     }

//     lightbox.addEventListener('click', (e) => {
//         if (e.target === lightbox) lightbox.classList.remove('active');
//     });
// }

// function initRevealAnimations() {
//     const observer = new IntersectionObserver((entries, observer) => {
//         entries.forEach(entry => {
//             if (entry.isIntersecting) {
//                 entry.target.classList.add('active');
//                 observer.unobserve(entry.target);
//             }
//         });
//     }, { threshold: 0.15 });

//     document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
// }

// function initFilterTabs() {
//     const filterBtns = document.querySelectorAll('.filter-btn');
//     filterBtns.forEach(btn => {
//         btn.addEventListener('click', () => {
//             filterBtns.forEach(b => b.classList.remove('active'));
//             btn.classList.add('active');
//         });
//     });
// }

// function initDropdown() {
//     const dropdowns = document.querySelectorAll('.dropdown');
//     dropdowns.forEach(dropdown => {
//         const toggle = dropdown.querySelector('.dropdown-toggle');
//         if (!toggle) return;

//         toggle.addEventListener('click', (e) => {
//             if (window.innerWidth < BLOG_CONFIG.mobileBreakpoint) {
//                 e.preventDefault();
//                 e.stopPropagation();
//                 dropdown.classList.toggle('active');
//             }
//         });
//     });
// }

// function initHeroCarousel() {
//     const slides = document.querySelectorAll('.hero-carousel .carousel-item');
//     if (slides.length < 2) return;
//     let current = 0;
//     setInterval(() => {
//         slides[current].classList.remove('active');
//         current = (current + 1) % slides.length;
//         slides[current].classList.add('active');
//     }, 4000);
// }

// document.addEventListener('DOMContentLoaded', () => {
//     initNavbar();
//     initMobileMenu();
//     initLightbox();
//     initRevealAnimations();
//     initFilterTabs();
//     initDropdown();
//     initHeroCarousel();
// });

// static/js/blog/component.js
function initNavbar() {
    const header = document.querySelector('header');
    if (!header) return;
    window.addEventListener('scroll', () => {
        header.classList.toggle('scrolled', window.scrollY > BLOG_CONFIG.scrollOffset);
    });
}

function initMobileMenu() {
    const mobileBtn = document.getElementById('mobileMenuBtn');
    const navLinks = document.getElementById('navLinks');
    if (!mobileBtn || !navLinks) return;

    mobileBtn.addEventListener('click', function (e) {
        e.preventDefault(); // mencegah perilaku default
        e.stopPropagation(); // mencegah event bubbling ke document
        navLinks.classList.toggle('show');
        // Ganti ikon
        if (navLinks.classList.contains('show')) {
            mobileBtn.innerHTML = '<i class="fa-solid fa-xmark"></i>';
        } else {
            mobileBtn.innerHTML = '<i class="fa-solid fa-bars-staggered"></i>';
        }
    });

    // Tutup menu saat klik di luar
    document.addEventListener('click', function (e) {
        if (!mobileBtn.contains(e.target) && !navLinks.contains(e.target)) {
            navLinks.classList.remove('show');
            mobileBtn.innerHTML = '<i class="fa-solid fa-bars-staggered"></i>';
        }
    });
}

function initLightbox() {
    const lightbox = document.querySelector('.lightbox');
    if (!lightbox) return;
    const lightboxImg = lightbox.querySelector('.lightbox-content');
    const closeBtn = lightbox.querySelector('.lightbox-close');
    document.querySelectorAll('.photo-item').forEach(item => {
        item.addEventListener('click', () => {
            const img = item.querySelector('img');
            if (img) {
                lightboxImg.src = img.src;
                lightbox.classList.add('active');
            }
        });
    });
    if (closeBtn) closeBtn.addEventListener('click', () => lightbox.classList.remove('active'));
    lightbox.addEventListener('click', (e) => { if (e.target === lightbox) lightbox.classList.remove('active'); });
}

function initRevealAnimations() {
    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) { entry.target.classList.add('active'); observer.unobserve(entry.target); }
        });
    }, { threshold: 0.15 });
    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
}

function initFilterTabs() {
    const btns = document.querySelectorAll('.filter-btn');
    btns.forEach(btn => {
        btn.addEventListener('click', () => {
            btns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });
}

function initDropdown() {
    const dropdowns = document.querySelectorAll('.dropdown');
    dropdowns.forEach(dropdown => {
        const toggle = dropdown.querySelector('.dropdown-toggle');
        if (!toggle) return;
        toggle.addEventListener('click', (e) => {
            if (window.innerWidth < BLOG_CONFIG.mobileBreakpoint) {
                e.preventDefault();
                e.stopPropagation();
                dropdown.classList.toggle('active');
            }
        });
    });
}

function initHeroCarousel() {
    const slides = document.querySelectorAll('.hero-carousel .carousel-item');
    if (slides.length < 2) return;
    let current = 0;
    setInterval(() => {
        slides[current].classList.remove('active');
        current = (current + 1) % slides.length;
        slides[current].classList.add('active');
    }, 4000);
}

document.addEventListener('DOMContentLoaded', () => {
    initNavbar();
    initMobileMenu();
    initLightbox();
    initRevealAnimations();
    initFilterTabs();
    initDropdown();
    initHeroCarousel();
});