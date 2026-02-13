/**
 * Strategic Synergy - Main Interactive Features
 * 1. Scroll Animations (IntersectionObserver)
 * 2. Animated Counters
 * 3. Back-to-top button
 * 4. Dark/Light mode toggle
 * 5. Mobile hamburger menu animation
 * 6. Hero image carousel
 */

document.addEventListener('DOMContentLoaded', () => {

    // ===== 1. SCROLL ANIMATIONS =====
    const scrollElements = document.querySelectorAll('.scroll-animate');

    const scrollObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('scroll-visible');
                // Add staggered delay for children
                const children = entry.target.querySelectorAll('.stagger-child');
                children.forEach((child, i) => {
                    child.style.transitionDelay = `${i * 0.1}s`;
                    child.classList.add('scroll-visible');
                });
            }
        });
    }, {
        threshold: 0.15,
        rootMargin: '0px 0px -50px 0px'
    });

    scrollElements.forEach(el => scrollObserver.observe(el));


    // ===== 2. ANIMATED COUNTERS =====
    const counters = document.querySelectorAll('.counter');
    let countersAnimated = false;

    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !countersAnimated) {
                countersAnimated = true;
                animateCounters();
            }
        });
    }, { threshold: 0.5 });

    const counterSection = document.querySelector('.impact-stats');
    if (counterSection) {
        counterObserver.observe(counterSection);
    }

    function animateCounters() {
        counters.forEach(counter => {
            const target = parseInt(counter.getAttribute('data-target'));
            const suffix = counter.getAttribute('data-suffix') || '';
            const duration = 2000;
            const step = target / (duration / 16);
            let current = 0;

            const updateCounter = () => {
                current += step;
                if (current < target) {
                    counter.textContent = Math.floor(current) + suffix;
                    requestAnimationFrame(updateCounter);
                } else {
                    counter.textContent = target + suffix;
                }
            };
            requestAnimationFrame(updateCounter);
        });
    }


    // ===== 3. BACK-TO-TOP BUTTON =====
    const backToTop = document.getElementById('back-to-top');
    if (backToTop) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 400) {
                backToTop.classList.add('visible');
            } else {
                backToTop.classList.remove('visible');
            }
        });

        backToTop.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }


    // ===== 4. DARK/LIGHT MODE TOGGLE =====
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;
    const savedTheme = localStorage.getItem('ss-theme');

    if (savedTheme === 'light') {
        body.classList.add('light-mode');
        if (themeToggle) themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            body.classList.toggle('light-mode');
            const isLight = body.classList.contains('light-mode');
            localStorage.setItem('ss-theme', isLight ? 'light' : 'dark');
            themeToggle.innerHTML = isLight
                ? '<i class="fas fa-moon"></i>'
                : '<i class="fas fa-sun"></i>';
        });
    }


    // ===== 5. MOBILE HAMBURGER MENU =====
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    if (hamburger && navLinks) {
        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('active');
            navLinks.classList.toggle('mobile-open');
            body.classList.toggle('nav-open');
        });

        // Close menu when clicking a link
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                hamburger.classList.remove('active');
                navLinks.classList.remove('mobile-open');
                body.classList.remove('nav-open');
            });
        });
    }


    // ===== 6. HERO IMAGE CAROUSEL =====
    const carousel = document.querySelector('.hero-carousel');
    if (carousel) {
        const slides = carousel.querySelectorAll('.carousel-slide');
        const dots = carousel.querySelectorAll('.carousel-dot');
        let currentSlide = 0;
        let autoplayInterval;

        function showSlide(index) {
            slides.forEach(s => s.classList.remove('active'));
            dots.forEach(d => d.classList.remove('active'));

            currentSlide = (index + slides.length) % slides.length;
            slides[currentSlide].classList.add('active');
            if (dots[currentSlide]) dots[currentSlide].classList.add('active');
        }

        function nextSlide() {
            showSlide(currentSlide + 1);
        }

        function startAutoplay() {
            autoplayInterval = setInterval(nextSlide, 5000);
        }

        function stopAutoplay() {
            clearInterval(autoplayInterval);
        }

        // Dot click handlers
        dots.forEach((dot, i) => {
            dot.addEventListener('click', () => {
                stopAutoplay();
                showSlide(i);
                startAutoplay();
            });
        });

        // Prev/Next buttons
        const prevBtn = carousel.querySelector('.carousel-prev');
        const nextBtn = carousel.querySelector('.carousel-next');

        if (prevBtn) {
            prevBtn.addEventListener('click', () => {
                stopAutoplay();
                showSlide(currentSlide - 1);
                startAutoplay();
            });
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                stopAutoplay();
                showSlide(currentSlide + 1);
                startAutoplay();
            });
        }

        // Pause on hover
        carousel.addEventListener('mouseenter', stopAutoplay);
        carousel.addEventListener('mouseleave', startAutoplay);

        // Initialize
        showSlide(0);
        startAutoplay();
    }


    // ===== HEADER SCROLL EFFECT =====
    const header = document.querySelector('.header');
    if (header) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                header.classList.add('header-scrolled');
            } else {
                header.classList.remove('header-scrolled');
            }
        });
    }


    // ===== 7. PAGE LOADER =====
    const pageLoader = document.getElementById('page-loader');
    if (pageLoader) {
        window.addEventListener('load', () => {
            setTimeout(() => {
                pageLoader.classList.add('loaded');
            }, 400);
        });
        // Fallback: hide after 3 seconds no matter what
        setTimeout(() => {
            pageLoader.classList.add('loaded');
        }, 3000);
    }


    // ===== 8. TESTIMONIAL SLIDER =====
    const testimonialTrack = document.querySelector('.testimonial-track');
    if (testimonialTrack) {
        const tCards = testimonialTrack.querySelectorAll('.testimonial-card');
        const tDots = document.querySelectorAll('.testimonial-dot');
        let currentTestimonial = 0;
        let testimonialInterval;

        function showTestimonial(index) {
            tCards.forEach(c => c.classList.remove('active'));
            tDots.forEach(d => d.classList.remove('active'));
            currentTestimonial = (index + tCards.length) % tCards.length;
            tCards[currentTestimonial].classList.add('active');
            if (tDots[currentTestimonial]) tDots[currentTestimonial].classList.add('active');
        }

        function startTestimonials() {
            testimonialInterval = setInterval(() => {
                showTestimonial(currentTestimonial + 1);
            }, 6000);
        }

        tDots.forEach((dot, i) => {
            dot.addEventListener('click', () => {
                clearInterval(testimonialInterval);
                showTestimonial(i);
                startTestimonials();
            });
        });

        showTestimonial(0);
        startTestimonials();
    }


    // ===== 9. PARALLAX SCROLL EFFECT =====
    const heroSection = document.querySelector('.hero');
    if (heroSection) {
        window.addEventListener('scroll', () => {
            const scrolled = window.scrollY;
            const heroHeight = heroSection.offsetHeight;
            if (scrolled < heroHeight) {
                const parallaxSpeed = scrolled * 0.3;
                heroSection.style.setProperty('--parallax-y', `${parallaxSpeed}px`);
                // Subtle opacity fade on hero content as user scrolls
                const heroContent = heroSection.querySelector('.hero-container');
                if (heroContent) {
                    const opacity = 1 - (scrolled / heroHeight) * 0.5;
                    heroContent.style.opacity = Math.max(opacity, 0.3);
                    heroContent.style.transform = `translateY(${parallaxSpeed * 0.2}px)`;
                }
            }
        });
    }

});
