document.addEventListener('DOMContentLoaded', function () {
    const logo = document.querySelector('.logo');
    const mainCta = document.querySelector('.cta-button');
    const mainTitle = document.querySelector('.emotion-cards__title');
    const mainHourBlocks = document.querySelectorAll('.hour-block');
    const mainTimeLabels = document.querySelectorAll('.time-label.text-secondary');
    const mainXAxisLabels = document.querySelectorAll('.d-flex.justify-content-between.x-axis-text');
    const mainStats = document.querySelectorAll('.stat');
    const mainSecondaryBtns = document.querySelectorAll('button.button-link');
    const cards = document.querySelectorAll('.card.card__wrapper')
    const noEmotions = document.querySelector('.no-emotions');

    const mainTl = gsap.timeline();
    mainTl.fromTo(logo,
        {opacity: 0},
        {opacity: 1, duration: 1, ease: 'power2.inOut'})
        .fromTo(mainCta,
            {opacity: 0},
            {opacity: 1, duration: 1, ease: 'power2.inOut'},
            '<')
        .fromTo(mainTimeLabels,
            {opacity: 0},
            {opacity: 1, duration: .4, stagger: .1, ease: 'power2.inOut'},
            '-=.3')
        .fromTo(mainXAxisLabels,
            {opacity: 0},
            {opacity: 1, duration: .4, stagger: .3, ease: 'power2.inOut'},
            '<')
        .fromTo(mainHourBlocks,
            {opacity: 0},
            {opacity: 1, duration: .1, stagger: .1, ease: 'power2.inOut'},
            '-=.2'
        )
        .fromTo(mainTitle,
            {clipPath: 'inset(0 0 100% 0)'},
            {opacity: 1, clipPath: 'inset(0 0 0% 0)', duration: 2, ease: 'power2.inOut'},
            '<')
        .fromTo(mainStats,
            {opacity: 0},
            {opacity: 1, duration: .5, stagger: .4, ease: 'power2.inOut'},
            '<');

    if (mainSecondaryBtns.length && cards.length) {
        mainTl.fromTo(mainSecondaryBtns,
            {opacity: 0},
            {opacity: 1, duration: .3, stagger: .2, ease: 'power2.inOut'},
            '<')
        .fromTo(cards,
            {opacity: 0},
            {opacity: 1, duration: 1, stagger: .2, ease: 'power2.inOut'},
            '<');
    }

    if (noEmotions) {
        mainTl.from(noEmotions, {
            opacity: 0,
            duration: 1,
            ease: "power2.out"
        });
    }
});

document.addEventListener('htmx:afterSwap', (e) => {
    if (e.detail.target.id === 'emotion-data') {
        const mainSecondaryBtns = document.querySelectorAll('button.button-link');
        const cards = document.querySelectorAll('.card.card__wrapper');

        // Reinitialize animations for buttons and cards
        const reloadTl = gsap.timeline();
        reloadTl.set(mainSecondaryBtns, {
            opacity: 1
        })
        reloadTl.fromTo(cards,
            {opacity: 0},
            {opacity: 1, duration: 1, stagger: 0.2, ease: 'power2.inOut'},
            '<');
    }
});


document.querySelectorAll('.cube-tooltip-wrapper').forEach(wrapper => {
    const tooltipWrapper = wrapper.querySelector('.cube-tooltip__wrapper');
    const cube = wrapper.querySelector('.cube');

    const updateTooltipPosition = () => {
        const cubeRect = cube.getBoundingClientRect();
        tooltipWrapper.style.left = `${cubeRect.left + cubeRect.width / 2}px`;
        tooltipWrapper.style.top = `${cubeRect.top - cubeRect.height / 2 + 35}px`;
    };

    // Show tooltip function
    const showTooltip = () => {
        updateTooltipPosition();
        tooltipWrapper.style.display = 'block'; // Ensure it’s visible
        window.addEventListener('scroll', updateTooltipPosition);
    };

    // Hide tooltip function
    const hideTooltip = () => {
        tooltipWrapper.style.display = 'none'; // Hide it
        window.removeEventListener('scroll', updateTooltipPosition);
    };

    // Desktop: Mouse events
    wrapper.addEventListener('mouseenter', showTooltip);
    wrapper.addEventListener('mouseleave', hideTooltip);

    // Mobile: Touch events
    wrapper.addEventListener('touchstart', (e) => {
        showTooltip();
    }, { passive: true });

    // Hide on touch outside or after a delay
    document.addEventListener('touchstart', (e) => {
        if (!wrapper.contains(e.target)) {
            hideTooltip();
        }
    }, { passive: true });
});