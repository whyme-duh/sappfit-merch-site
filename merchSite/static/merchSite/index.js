
setTimeout(function(){
    const alert = document.getElementById('alert-msg');
    if(alert){
        alert.style.display = "none";
    }

}, 10000)


function navbarFunction() {
  var x = document.getElementById("nav-links");
  if (x.className === "nav-links") {
    x.className += " responsive";
  } else {
    x.className = "nav-links";
  }
  
}

// for tracking model

// const trackOrderOverlay = document.getElementById('trackOrderOverlay');
// if (trackOrderOverlay){
//     document.getElementById('body').style.overflow = "hidden";
// }
// else{
//     document.getElementById('body').style.overflow = "visible";
    

// }

// product detail page

const addToCartBtn = document.getElementById('add-to-cart-btn');
addToCartBtn.addEventListener('mouseenter', () => {
    addToCartBtn.innerHTML =`<i style="font-size:24px" class="fa">&#xf07a;</i>`;
})
addToCartBtn.addEventListener('mouseleave', () => {
    addToCartBtn.innerText = "Add to Bag";
})

function showReviews(){
    const reviewOverlay = document.getElementById('reviews-container');
    reviewOverlay.style.display = "flex";
    // document.getElementById('body').style.overflow = "hidden";
}

function closeShowReviews(){
    const reviewOverlay = document.getElementById('reviews-container');
    reviewOverlay.style.display = "none";
    // document.getElementById('body').style.overflow = "visible";

}



function closeTrackModal() {
    const modalOverlay = document.getElementById('trackOrderOverlay');
    modalOverlay.style.display = "none";
}

function cancelOrderInTrackOrderModel(option){
    const cancelForm = document.getElementById('track-order-modal-box');

    if (option == 'open'){
        cancelForm.style.display = "block";
    }else if (option == "close"){
        cancelForm.style.display = "none";
    }
    else{
        alert('incorrect');
    }
}

function addToCart(actionUrl){
    const productDetailForm = document.getElementById('productDetailForm');
    productDetailForm.action = actionUrl;
}

function directCartToCheckout(actionUrl){
    
    const productDetailForm = document.getElementById('productDetailForm');
    productDetailForm.action = actionUrl;
}

function openImportOrderModal(){
    const modalOverlay = document.getElementById('importOrderModalOverlay');
    modalOverlay.classList.add('active');
}

function closeImportOrderModal(){
    const modalOverlay = document.getElementById('importOrderModalOverlay');
    modalOverlay.classList.remove('active');
}



function openCancelModal(actionUrl) {
    const cancelForm = document.getElementById('cancelOrderForm');
    const modalOverlay = document.getElementById('cancelModalOverlay');
    

    cancelForm.setAttribute('action', actionUrl);
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

function openReturnModal(actionUrl, productName ,productId, productSize, productQuantity) {
    const inputProductName = document.getElementById('product-name');
    const inputProductSize = document.getElementById('product-size');
    const inputProductQuantity = document.getElementById('product-quantity');
    const returnForm = document.getElementById('returnForm');
    const modalOverlay = document.getElementById('returnModalOverlay');
    const modalReturnProduct = document.getElementById('modalReturnProduct');

    inputProductName.value = productName;
    inputProductSize.value = productSize;
    inputProductQuantity.value = productQuantity;
    
    returnForm.action = actionUrl;
    modalReturnProduct.innerText = "#" + productId;
    modalOverlay.classList.add('active');
}

function closeReturnModal() {
    const modalOverlay = document.getElementById('returnModalOverlay');
    modalOverlay.classList.remove('active');
}



// backdrop effect when seeing the result of tracked orders

const trackResult = document.getElementById('track-result');
const trackResultBackground = document.getElementById('track-order-container');
function closeThis(){
    trackResult.style.display = "hide";
}
if (trackResult){
    trackResultBackground.style.display = "flex";
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
if (track){
    const slides = Array.from(track.children);
    const nextButton = document.querySelector('.carousel__button-container--next');
    const prevButton = document.querySelector('.carousel__button-container--prev');
    const indicatorsNav = document.querySelector('.carousel__indicator-container');
    const indicators = Array.from(indicatorsNav.children);
    const slideWidth = slides[0].getBoundingClientRect().width;
    // find the width to move

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



}

// product detail part

const minusBtn = document.getElementById('minus-btn');
const plusBtn = document.getElementById('plus-btn');
const quantityAmt = document.getElementById('quantity');

minusBtn.addEventListener('click', ()=>{
    quantityAmt.value -= 1;
})
plusBtn.addEventListener('click', ()=>{
    let quantityVal = parseInt(quantityAmt.value, 10);
    quantityVal += 1;
    quantityAmt.value = quantityVal;
})


// window.onclick = function(event) {
//     if (modalOverlay){
//         if (event.target === modalOverlay) {
//             closeCancelModal();
//             closeTrackModal();
//         }
//     }

    
// }
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
const relatedProd = document.getElementById("related-prod");

if (reviewSection && relatedProd){
    relatedProd.style.marginTop = "5em";
}
// else{
//     relatedProd.style.marginTop = "20em";

// }




