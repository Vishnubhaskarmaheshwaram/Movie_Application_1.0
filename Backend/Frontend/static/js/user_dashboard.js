// Check if user is logged in
if (!localStorage.getItem('token')) {
    window.location.href = 'login.html';
}

const token = localStorage.getItem('token');
const moviesListElement = document.getElementById('movies-list');
const reviewFormContainer = document.getElementById('review-form-container');
const reviewForm = document.getElementById('review-form');
const reviewsContainer = document.getElementById('reviews-container');
const logoutBtn = document.getElementById('logout-btn');

// Fetch and display movies
async function fetchMovies() {
    try {
        const response = await fetch('http://localhost:8000/movies/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (!response.ok) throw new Error('Failed to fetch movies');
        const movies = await response.json();
        displayMovies(movies);
    } catch (error) {
        console.error('Error fetching movies:', error);
        moviesListElement.innerHTML = '<p>Failed to load movies. Please try again later.</p>';
    }
}

function displayMovies(movies) {
    moviesListElement.innerHTML = '<h3>Movies</h3>';
    movies.forEach(movie => {
        const movieElement = document.createElement('div');
        movieElement.innerHTML = `
            <h4>${movie.title}</h4>
            <p>Director: ${movie.director}</p>
            <p>Genre: ${movie.genre}</p>
            <button onclick="showReviewForm(${movie.id})">Leave a Review</button>
            <button onclick="showReviews(${movie.id})">Show Reviews</button>
        `;
        moviesListElement.appendChild(movieElement);
    });
}

function showReviewForm(movieId) {
    reviewFormContainer.style.display = 'block';
    document.getElementById('movie-id').value = movieId;
}

async function submitReview(e) {
    e.preventDefault();
    const movieId = document.getElementById('movie-id').value;
    const rating = document.getElementById('rating').value;
    const reviewText = document.getElementById('review-text').value;

    try {
        const response = await fetch('http://localhost:8000/reviews/', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ movie_id: parseInt(movieId), rating: parseInt(rating), review_text: reviewText })
        });
        if (!response.ok) throw new Error('Failed to submit review');
        alert('Review submitted successfully!');
        reviewForm.reset();
        reviewFormContainer.style.display = 'none';
        showReviews(movieId);
    } catch (error) {
        console.error('Error submitting review:', error);
        alert('Failed to submit review. Please try again.');
    }
}

async function showReviews(movieId) {
    try {
        const response = await fetch(`http://localhost:8000/movies/${movieId}/reviews`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (!response.ok) throw new Error('Failed to fetch reviews');
        const reviews = await response.json();
        displayReviews(reviews);
    } catch (error) {
        console.error('Error fetching reviews:', error);
        reviewsContainer.innerHTML = '<p>Failed to load reviews. Please try again later.</p>';
    }
}

function displayReviews(reviews) {
    reviewsContainer.innerHTML = '<h3>Reviews</h3>';
    if (reviews.length === 0) {
        reviewsContainer.innerHTML += '<p>No reviews yet for this movie.</p>';
    } else {
        reviews.forEach(review => {
            const reviewElement = document.createElement('div');
            reviewElement.innerHTML = `
                <p>Rating: ${review.rating}/5</p>
                <p>${review.review_text}</p>
                <hr>
            `;
            reviewsContainer.appendChild(reviewElement);
        });
    }
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    window.location.href = 'login.html';
}

// Event listeners
document.addEventListener('DOMContentLoaded', fetchMovies);
reviewForm.addEventListener('submit', submitReview);
logoutBtn.addEventListener('click', logout);