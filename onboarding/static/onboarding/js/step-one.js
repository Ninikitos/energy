document.addEventListener('DOMContentLoaded', function () {
    const logo = document.querySelector('.logo');
    const stepOneTitle = document.querySelector('.section__title');
    const stepOneSubTitle = document.querySelector('.section__subtitle');
    const cards = document.querySelectorAll('.card.card-button');
    const stepOneTl = gsap.timeline();
    stepOneTl.fromTo(stepOneTitle,
        {clipPath: 'inset(0 0 100% 0)'},
        {opacity: 1, clipPath: 'inset(0 0 0% 0)', duration: 3, ease: 'power2.inOut'},
        '-=.8')
        .fromTo(stepOneSubTitle,
            {clipPath: 'inset(0 0 100% 0)'},
            {opacity: 1, clipPath: 'inset(0 0 0% 0)', duration: 2, ease: 'power2.inOut'},
            '-=1.2')
        .fromTo(logo,
            {opacity: 0},
            {opacity: 1, duration: 1, ease: 'power2.inOut'},
            '-=1.3')
        .fromTo(cards,
            {opacity: 0},
            {
                opacity: 1,
                duration: 1,
                stagger: 0.2,
                ease: 'power2.inOut',
                onComplete: () => cards.forEach(card => card.classList.remove('pointer-events-disable'))
            },
            '-=1.4'
        );
});