document.addEventListener('DOMContentLoaded', function () {
    const logo = document.querySelector('.logo');
    const stepThreeTitle = document.querySelector('.section__title');
    const stepThreeSubTitle = document.querySelector('.section__subtitle');
    const stepThreeInput = document.querySelector('#user_name');
    const stepThreeTextarea = document.querySelector('#emotion_reason');
    const stepThreeCta = document.querySelector('.cta-button');
    const stepThreeSecondaryBtn = document.querySelector('.button-link.button-link-fixed-height-steps');

    const stepThreeTl = gsap.timeline();
    stepThreeTl.fromTo(stepThreeTitle,
        {clipPath: 'inset(0 0 100% 0)'},
        {opacity: 1, clipPath: 'inset(0 0 0% 0)', duration: 3, ease: 'power2.inOut'},
        '-=.8')
        .fromTo(stepThreeSubTitle,
            {clipPath: 'inset(0 0 100% 0)'},
            {opacity: 1, clipPath: 'inset(0 0 0% 0)', duration: 2, ease: 'power2.inOut'},
            '-=1.2')
        .fromTo(logo,
            {opacity: 0},
            {opacity: 1, duration: 1, ease: 'power2.inOut'},
            '-=1.3')
        .fromTo(stepThreeInput,
            {opacity: 0},
            {opacity: 1, duration: 1, ease: 'power2.inOut',
            onComplete: () => stepThreeInput.classList.remove('pointer-events-disable')},
            '-=1.4'
        )
        .fromTo(stepThreeTextarea,
            {opacity: 0},
            {opacity: 1, duration: 1, ease: 'power2.inOut',
            onComplete: () => stepThreeTextarea.classList.remove('pointer-events-disable')},
            '-=1.5'
        )
        .fromTo(stepThreeCta,
            {opacity: 0},
            {opacity: 1, duration: 1, ease: 'power2.inOut',
            onComplete: () => stepThreeCta.classList.remove('pointer-events-disable')},
            '-=1.5')
        .fromTo(stepThreeSecondaryBtn,
            {opacity: 0},
            {opacity: 1, duration: 1, ease: 'power2.inOut',
            onComplete: () => stepThreeSecondaryBtn.classList.remove('pointer-events-disable')},
            '<');
});

function validateInput() {
    const areatextarea = document.querySelector("#emotion_reason");
    const areatext = document.querySelector("#emotion_reason").value.length;
    const textcount = document.querySelector("#textcount");
    const wordcount = document.querySelector("#words_count");
    textcount.innerHTML = areatext;

    if (areatext > 256) {
        textcount.classList.add("text-danger");
        areatextarea.classList.add("textarea_danger");
    } else {
        textcount.classList.remove("text-danger");
        areatextarea.classList.remove("textarea_danger");
    }

    if (areatext < 1) {
        wordcount.classList.add("d-none");
    } else {
        wordcount.classList.remove("d-none");
    }
}