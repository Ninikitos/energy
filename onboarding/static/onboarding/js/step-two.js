document.addEventListener('DOMContentLoaded', function () {
    const logo = document.querySelector('.logo');
    const stepTwoTitle = document.querySelector('.section__title');
    const stepTwoSubTitle = document.querySelector('.section__subtitle');
    const cards = document.querySelectorAll('.emotions__card');
    const error = document.querySelector('.alert.alert-danger');
    const stepTwoCta = document.querySelector('.cta-button');
    const stepTwoSecondaryBtn = document.querySelector('.button-link.button-link-fixed-height-steps');

    const stepTwoTl = gsap.timeline();
    stepTwoTl.fromTo(stepTwoTitle, {clipPath: 'inset(0 0 100% 0)'}, {
        opacity: 1,
        clipPath: 'inset(0 0 0% 0)',
        duration: 2,
        ease: 'power2.inOut'
    }, '-=.8')
        .fromTo(stepTwoSubTitle, {clipPath: 'inset(0 0 100% 0)'}, {
            opacity: 1,
            clipPath: 'inset(0 0 0% 0)',
            duration: 2,
            ease: 'power2.inOut'
        }, '-=1.2')
        .fromTo(logo, {opacity: 0}, {opacity: 1, duration: 1, ease: 'power2.inOut'}, '-=1.3')
        .fromTo(cards, {opacity: 0}, {
            opacity: 1,
            duration: .4,
            stagger: .2,
            ease: 'power2.inOut',
            onComplete: () => cards.forEach(card => card.classList.remove('pointer-events-disable'))
        }, '-=1.4')
        .fromTo(error, {opacity: 0, y: 10},
            {opacity: 1, y: 0, duration: 1, ease: 'power2.inOut'}, '<=1')
        .fromTo(stepTwoCta, {opacity: 0},
            {opacity: 1, duration: 1, ease: 'power2.inOut',
            onComplete: () => stepTwoCta.classList.remove('pointer-events-disable')}, '-=1.5')
        .fromTo(stepTwoSecondaryBtn, {opacity: 0},
            {opacity: 1, duration: 1, ease: 'power2.inOut',
            onComplete: () => stepTwoSecondaryBtn.classList.remove('pointer-events-disable')}, '<');
});