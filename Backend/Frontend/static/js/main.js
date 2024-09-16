document.addEventListener('DOMContentLoaded', async function() {
const role = localStorage.getItem('role');
const token = localStorage.getItem('token');

if (!token) {
window.location.href = '/static/index.html';
}

if (role === 'Admin') {
document.getElementById('movie-form').addEventListener('submit', async function(e) {
e.preventDefault();

const title = document.getElementById('movie-title').value;
const director = document.getElementById('director').value;
const genre = document.getElementById('genre').value;

const response = await fetch('http://localhost:8000/movies/', {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ title, director, genre })
});

if (response.ok) {
    alert('Movie created successfully!');
} else {
    alert('Failed to create movie!');
}
});

document.getElementById('showtime-form').addEventListener('submit', async function(e) {
e.preventDefault();

const movie_id = document.getElementById('movie-id').value;
const start_time = document.getElementById('start-time').value;

const response = await fetch('http://localhost:8000/showtimes/', {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ movie_id, start_time })
});

if (response.ok) {
    alert('Showtime created successfully!');
} else {
    alert('Failed to create showtime!');
}
});
} else {
const moviesList = document.getElementById('movies-list');

// Fetch and display movies
const response = await fetch('/movies/', {
headers: {
    'Authorization': `Bearer ${token}`
}
});

if (response.ok) {
const movies = await response.json();
movies.forEach(movie => {
    const movieElement = document.createElement('div');
    movieElement.classList.add('movie');
    movieElement.innerHTML = `<h3>${movie.title}</h3><p>Directed by: ${movie.director}</p><p>Genre: ${movie.genre}</p>`;
    moviesList.appendChild(movieElement);
});
}

document.getElementById('review-form').addEventListener('submit', async function(e) {
e.preventDefault();

const movie_id = document.getElementById('movie-id').value;
const rating = document.getElementById('rating').value;
const review_text = document.getElementById('review-text').value;

const response = await fetch('http://localhost:8000/reviews/', {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ movie_id, rating, review_text })
});

if (response.ok) {
    alert('Review submitted successfully!');
} else {
    alert('Failed to submit review!');
}
});
}
});
