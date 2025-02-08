document.addEventListener('DOMContentLoaded', function () {
    // Preloader
    const items = document.querySelectorAll('.preloader__item');
    const preloaderTl = gsap.timeline({repeat: 0});
    const preloader = document.querySelector('.preloader');
    const preloaderLight = document.querySelector('.preloader__inner-light');
    const preloaderGreen = document.querySelector('.preloader__inner-green');
    const preloaderRed = document.querySelector('.preloader__inner-red');

    // Hero
    const logo = document.querySelector('.logo');
    const heroTitle = document.querySelector('.section__title');
    const heroSubTitle = document.querySelector('.section__subtitle');
    const heroCta = document.querySelector('.cta-button');
    const heroSecondaryBtn = document.querySelector('.button-link.button-link-fixed-height');
    const heroEmotionCards = document.querySelectorAll('.emotions-list__item');


    items.forEach((item, index) => {
        const text = item.querySelector('p');
        const mark = item.querySelector('.preloader__item .mark');

        const itemTl = gsap.timeline();

        itemTl.fromTo(
            text,
            {y: -20, opacity: 0},
            {y: 0, opacity: 1, duration: 0.3, ease: 'power2.out'}
        );

        itemTl.fromTo(
            mark,
            {x: -40, opacity: 0},
            {x: 0, opacity: 1, duration: 0.5, ease: 'power1.inOut'},
            '-=0.3'
        );

        itemTl.to(
            [text, mark],
            {y: 20, duration: 0.3, ease: 'power1.inOut'}
        );

        itemTl.to(
            item,
            {opacity: 0, duration: 0.3, ease: 'power2.out'}
        );

        preloaderTl.add(itemTl, index * 1.1);
    });

    preloaderTl.addLabel('endItems');

    preloaderTl.fromTo(
        preloaderLight,
        {clipPath: 'inset(0% 0% 0% 0%)'}, // Start clip from bottom
        {clipPath: 'inset(0% 0% 100% 0%)', duration: 0.6, ease: 'power2.inOut'}
    );

    preloaderTl.fromTo(
        preloaderGreen,
        {clipPath: 'inset(0% 0% 0% 0%)'},
        {clipPath: 'inset(0% 0% 100% 0%)', duration: 0.6, ease: 'power2.inOut', delay: 0.3},
        '-=.8'
    );

    preloaderTl.fromTo(
        preloaderRed,
        {clipPath: 'inset(0% 0% 0% 0%)'},
        {clipPath: 'inset(0% 0% 100% 0%)', duration: 0.6, ease: 'power2.inOut', delay: 0.3},
        '-=.8'
    );

    preloaderTl.eventCallback('onComplete', () => {

        const heroTl = gsap.timeline();
        gsap.set(preloader,
            {display: 'none'});

        heroTl.fromTo(heroTitle,
                {clipPath: 'inset(0 0 100% 0)'},
                {opacity: 1, clipPath: 'inset(0 0 0% 0)', duration: 3, ease: 'power2.inOut'},
                '-=.8')
            .fromTo(heroSubTitle,
                {clipPath: 'inset(0 0 100% 0)'},
                {opacity: 1, clipPath: 'inset(0 0 0% 0)', duration: 2, ease: 'power2.inOut'},
                '-=1.2')
            .fromTo(heroCta,
                {opacity: 0},
                {
                    opacity: 1,
                    duration: 1,
                    ease: 'power2.inOut',
                    onComplete: () => heroCta.classList.remove('pointer-events-disable')
                },
                '-=1.7')
            .fromTo(heroSecondaryBtn,
                {opacity: 0},
                {
                    opacity: 1,
                    duration: 1,
                    ease: 'power2.inOut',
                    onComplete: () => heroSecondaryBtn.classList.remove('pointer-events-disable')
                },
                '-=1.8')
            .fromTo(heroEmotionCards,
                {opacity: 0, y: -4},
                {opacity: 1, y: 0, duration: .4, stagger: .2, ease: 'power2.inOut'},
                '-=2.3')
            .fromTo(logo,
                {opacity: 0},
                {opacity: 1, duration: 1, ease: 'power2.inOut'},
                '-=2.8');
    });
});