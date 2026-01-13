const { act } = require("react");

setTimeout(function(){
    const alert = document.getElementById('alert-msg');

    alert.style.display = "none";
}, 4000)


function navbarFunction() {
  var x = document.getElementById("nav-links");
  if (x.className === "nav-links") {
    x.className += " responsive";
  } else {
    x.className = "nav-links";
  }
  
}

function openCancelModal(actionUrl, orderId) {
    const cancelForm = document.getElementById('cancelForm');
    const modalOverlay = document.getElementById('cancelModalOverlay');
    const modalOrderIdSpan = document.getElementById('modalOrderId');

    cancelForm.action = actionUrl;
    modalOrderIdSpan.innerText = "#" + orderId;
    modalOverlay.classList.add('active');
}

function closeCancelModal() {
    const modalOverlay = document.getElementById('cancelModalOverlay');
    modalOverlay.classList.remove('active');
}

function toggleOtherReason(selectElement) {
    const otherReasonGroup = document.getElementById('otherReasonGroup');

    if (selectElement.value === 'Other') {
        otherReasonGroup.style.display = 'block';
    } else {
        otherReasonGroup.style.display = 'none';
    }
}

function openReturnModal(actionUrl, productName) {
    const returnForm = document.getElementById('returnForm');
    const modalOverlay = document.getElementById('returnModalOverlay');
    const modalReturnProduct = document.getElementById('modalReturnProduct');
    console.log(actionUrl, productName);
    returnForm.action = actionUrl;
    modalReturnProduct.innerText = "#" + productName;
    modalOverlay.classList.add('active');
}

function closeReturnModal() {
    const modalOverlay = document.getElementById('returnModalOverlay');
    modalOverlay.classList.remove('active');
}




window.onclick = function(event) {
    if (event.target === modalOverlay) {
        closeCancelModal();
    }
}
// backdrop effect when seeing the result of tracked orders

const trackResult = document.getElementById('track-result');
const trackResultBackground = document.getElementById('track-order-container');
function closeThis(){
    trackResult.style.display = "hide";
}
if (trackResult){
    console.log(trackResult, trackResultBackground);
    trackResultBackground.style.display = "fle";
}

// eye sight for password

const eyeSlash = document.getElementById("eye-slash");
const eyeSlashPassword1 = document.getElementById("eye-slash-password1");
const eyeSlashPassword2 = document.getElementById("eye-slash-password2");
const eye = document.getElementById("eye");
const eyepassword1 = document.getElementById("eye-password1");
const eyepassword2 = document.getElementById("eye-password2");

if (eyeSlashPassword1){
    eyeSlashPassword1.addEventListener("click", function(){
    const passwordField1 = document.getElementById("id_password1");
    passwordField1.type = "text";
    eyeSlashPassword1.style.display = "none";
    eyepassword1.style.display = "block";
})
}
if(eye){
    eye.addEventListener("click", function(){
    const passwordField = document.getElementById("id_password");
    passwordField.type = "password";
    eyeSlash.style.display = "block";
    eye.style.display = "none";
})
}


function showPassword(hiddenId, iId, passwordField){
    const eyeIcon = document.getElementById(hiddenId);
    const passField = document.getElementById(passwordField);
    passField.type = "text";
    eyeIcon.style.display = "block";
    const eyeSlash = document.getElementById(iId);
    eyeSlash.style.display = "none";

}

function hidePassword(hiddenId, iId, passwordField){
    const eyeIcon = document.getElementById(iId);
    const passField = document.getElementById(passwordField);
    const eyeSlash = document.getElementById(hiddenId);
    passField.type = "password";
    eyeIcon.style.display = "none";
    eyeSlash.style.display = "block";

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

// document.addEventListener("DOMContentLoaded", () => {
//     // Select all review cards and the arrows
//     const reviewCards = document.querySelectorAll(".review-card");
//     const leftArrow = document.getElementById("left-arrow");
//     const rightArrow = document.getElementById("right-arrow");
    
//     // Initialize the current review index
//     let currentReviewIndex = 0;
    
//     // Function to show a specific review and hide others
//     const showReview = (index) => {
//         // Loop through all review cards
//         reviewCards.forEach((card, i) => {
//             // If the current card's index matches the desired index, show it
//             if (i === index) {
//                 card.style.display = "block";
//             } else {
//                 // Otherwise, hide the card
//                 card.style.display = "none";
//             }
//         });
//     };
    
//     // Initial call to show the first review
//     showReview(currentReviewIndex);
    
//     // Event listener for the left arrow
//     leftArrow.addEventListener("click", () => {
//         // Decrement the index. If it goes below zero, wrap around to the last review.
//         currentReviewIndex = (currentReviewIndex - 1 + reviewCards.length) % reviewCards.length;
//         showReview(currentReviewIndex);
//     });
    
//     // Event listener for the right arrow
//     rightArrow.addEventListener("click", () => {
//         // Increment the index. If it goes past the last review, wrap around to the first.
//         currentReviewIndex = (currentReviewIndex + 1) % reviewCards.length;
//         showReview(currentReviewIndex);
//     });

//     // Optional: Add hover functionality to show/hide arrows
//     const reviewsContainer = document.querySelector(".reviews");
//     const arrowsContainer = document.getElementById("arrows");

//     if (arrowsContainer) {
//         reviewsContainer.addEventListener("mouseenter", () => {
//             arrowsContainer.style.display = "flex";
//         });
//         reviewsContainer.addEventListener("mouseleave", () => {
//             arrowsContainer.style.display = "none";
//         });
//     }
// });



const reviewSection = document.getElementById("reviews");
if (reviewSection){
    const relatedProd = document.getElementById("related-prod");
    relatedProd.style.marginTop = "5em";
}
else{
    const relatedProd = document.getElementById("related-prod");
    relatedProd.style.marginTop = "20em";

}




