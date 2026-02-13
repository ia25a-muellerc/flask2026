document.addEventListener('DOMContentLoaded', function () {
    const rateButton = document.querySelector('.rateButton');
    const submitRatingBtn = document.querySelector('.submit-rating-btn');
    const closeBtn = document.querySelector('.close-btn');
    const cancelButton = document.querySelector('.cancelButton');
    const stars = document.querySelectorAll('.star');
    const ratingSection = document.querySelector('.rating-section');
    const ratingText = document.getElementById('ratingText');
    const buttonContainer = document.querySelector('.button-container');

    let selectedRating = 0;
    const ratingLabels = {
        1: 'Poor',
        2: 'Not good',
        3: 'Okay',
        4: 'Good',
        5: 'Excellent!'
    };

    rateButton.addEventListener('click', function (e) {
        e.preventDefault();
        ratingSection.style.display = 'block';
        buttonContainer.style.display = 'none';
        selectedRating = 0;
        updateStars();
    });

    stars.forEach(star => {
        star.addEventListener('click', function () {
            selectedRating = this.getAttribute('data-value');
            updateStars();
            ratingText.textContent = ratingLabels[selectedRating];
            ratingText.style.color = '#f58800';
        });

        star.addEventListener('mouseover', function () {
            const hoverValue = this.getAttribute('data-value');
            stars.forEach(s => {
                if (s.getAttribute('data-value') <= hoverValue) {
                    s.classList.add('hovered');
                } else {
                    s.classList.remove('hovered');
                }
            });
        });
    });

    stars.forEach(star => {
        star.addEventListener('mouseout', function () {
            stars.forEach(s => {
                s.classList.remove('hovered');
            });
            updateStars();
        });
    });

    function updateStars() {
        stars.forEach(star => {
            const value = star.getAttribute('data-value');
            if (value <= selectedRating) {
                star.classList.add('active');
            } else {
                star.classList.remove('active');
            }
        });
    }

    submitRatingBtn.addEventListener('click', function () {
        if (selectedRating === 0) {
            ratingText.textContent = 'Please select a rating!';
            ratingText.style.color = '#ff6b6b';
            return;
        }

        ratingText.textContent = `Thank you! You rated ${selectedRating} star${selectedRating !== 1 ? 's' : ''}`;
        ratingText.style.color = '#4ade80';

        submitRatingBtn.disabled = true;
        submitRatingBtn.style.opacity = '0.6';

        setTimeout(() => {
            window.location.href = '/orders';
        }, 1500);
    });
});
