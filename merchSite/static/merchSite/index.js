
const alert = document.getElementById('alert-msg');
console.log(alert);
setTimeout(function(){
    alert.style.display = "none";
}, 2000)


function navbarFunction() {
  var x = document.getElementById("nav-links");
  if (x.className === "nav-links") {
    x.className += " responsive";
  } else {
    x.className = "nav-links";
  }
}
//Carousel

const track = document.querySelector('.carousel__track');
const slides = Array.from(track.children);
const nextButton = document.querySelector('.carousel__button-container--next');
const prevButton = document.querySelector('.carousel__button-container--prev');
const indicatorsNav = document.querySelector('.carousel__indicator-container');
const indicators = Array.from(indicatorsNav.children);

// find the width to move
const slideWidth = slides[0].getBoundingClientRect().width;

//Setting the slides in position
const setSlidePosition = (slide, index) => {
    slide.style.left = slideWidth * index + 'px';
}

slides.forEach(setSlidePosition);

//moveToSlide function
const moveToSlide = (track, currentSlide, targetSlide) => {
    track.style.transform = 'translateX(-' + targetSlide.style.left + ')';
    currentSlide.classList.remove('current-slide');
    targetSlide.classList.add('current-slide');
}

const updateIndicators = (currentIndi, targetIndi) => {
    currentIndi.classList.remove('current-slide');
    targetIndi.classList.add('current-slide');
};


//Show/Hide arrows function
const showHideArrows = (targetIndex, prevButton, nextButton, slides) => {
    if (targetIndex === 0) {
        prevButton.classList.add('is-hidden');
        nextButton.classList.remove('is-hidden');
    } else if (targetIndex === slides.length - 1) {
        prevButton.classList.remove('is-hidden');
        nextButton.classList.add('is-hidden');
    } else {
        prevButton.classList.remove('is-hidden');
        nextButton.classList.remove('is-hidden');
    }
}

prevButton.addEventListener('click', e => {
    const currentSlide = track.querySelector('.current-slide');
    const prevSlide = currentSlide.previousElementSibling;
    const currentIndi = indicatorsNav.querySelector('.current-slide');
    const prevIndi = currentIndi.previousElementSibling;
    const prevIndex = slides.findIndex(slide => slide === prevSlide);



    moveToSlide(track, currentSlide, prevSlide);
    updateIndicators(currentIndi, prevIndi);
    showHideArrows(prevIndex, prevButton, nextButton, slides);


});

nextButton.addEventListener('click', e => {
    const currentSlide = track.querySelector('.current-slide');
    const nextSlide = currentSlide.nextElementSibling;
    const currentIndi = indicatorsNav.querySelector('.current-slide');
    const nextIndi = currentIndi.nextElementSibling;
    const nextIndex = slides.findIndex(slide => slide === nextSlide);


    moveToSlide(track, currentSlide, nextSlide);
    updateIndicators(currentIndi, nextIndi);
    showHideArrows(nextIndex, prevButton, nextButton, slides);
});


indicatorsNav.addEventListener('click', e => {
    console.log('funker');
    const targetIndi = e.target.closest('div');

    if (!targetIndi) return;

    const currentSlide = track.querySelector('.current-slide');
    const currentIndi = indicatorsNav.querySelector('.current-slide');
    const targetIndex = indicators.findIndex(dot => dot === targetIndi);
    const targetSlide = slides[targetIndex];


    moveToSlide(track, currentSlide, targetSlide);
    updateIndicators(currentIndi, targetIndi);
    showHideArrows(targetIndex, prevButton, nextButton, slides);
})
document.addEventListener("DOMContentLoaded", () => {
    // Select all review cards and the arrows
    const reviewCards = document.querySelectorAll(".review-card");
    const leftArrow = document.getElementById("left-arrow");
    const rightArrow = document.getElementById("right-arrow");
    
    // Initialize the current review index
    let currentReviewIndex = 0;
    
    // Function to show a specific review and hide others
    const showReview = (index) => {
        // Loop through all review cards
        reviewCards.forEach((card, i) => {
            // If the current card's index matches the desired index, show it
            if (i === index) {
                card.style.display = "block";
            } else {
                // Otherwise, hide the card
                card.style.display = "none";
            }
        });
    };
    
    // Initial call to show the first review
    showReview(currentReviewIndex);
    
    // Event listener for the left arrow
    leftArrow.addEventListener("click", () => {
        // Decrement the index. If it goes below zero, wrap around to the last review.
        currentReviewIndex = (currentReviewIndex - 1 + reviewCards.length) % reviewCards.length;
        showReview(currentReviewIndex);
    });
    
    // Event listener for the right arrow
    rightArrow.addEventListener("click", () => {
        // Increment the index. If it goes past the last review, wrap around to the first.
        currentReviewIndex = (currentReviewIndex + 1) % reviewCards.length;
        showReview(currentReviewIndex);
    });

    // Optional: Add hover functionality to show/hide arrows
    const reviewsContainer = document.querySelector(".reviews");
    const arrowsContainer = document.getElementById("arrows");

    if (arrowsContainer) {
        reviewsContainer.addEventListener("mouseenter", () => {
            arrowsContainer.style.display = "flex";
        });
        reviewsContainer.addEventListener("mouseleave", () => {
            arrowsContainer.style.display = "none";
        });
    }
});




