document.addEventListener('DOMContentLoaded', function() {
    const token = localStorage.getItem('token');
    const role = localStorage.getItem('role');

    if (!token || role !== 'Admin') {
        window.location.href = '/static/index.html';
        return;
    }

    const movieForm = document.getElementById('movie-form');
    const showtimeForm = document.getElementById('showtime-form');
    const usersListElement = document.getElementById('users-list');
    const logoutBtn = document.getElementById('logout-btn');

    movieForm.addEventListener('submit', createMovie);
    showtimeForm.addEventListener('submit', createShowtime);
    logoutBtn.addEventListener('click', logout);

    fetchUsers();

    async function createMovie(e) {
        e.preventDefault();
        const title = document.getElementById('movie-title').value;
        const director = document.getElementById('director').value;
        const genre = document.getElementById('genre').value;

        try {
            const response = await fetch('http://localhost:8000/movies/', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ title, director, genre })
            });

            if (!response.ok) throw new Error('Failed to create movie');
            alert('Movie created successfully!');
            movieForm.reset();
        } catch (error) {
            console.error('Error creating movie:', error);
            alert('Failed to create movie. Please try again.');
        }
    }

    async function createShowtime(e) {
        e.preventDefault();
        const movie_id = document.getElementById('movie-id').value;
        const start_time = document.getElementById('start-time').value;

        try {
            const response = await fetch('http://localhost:8000/showtimes/', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ movie_id: parseInt(movie_id), start_time })
            });

            if (!response.ok) throw new Error('Failed to create showtime');
            alert('Showtime created successfully!');
            showtimeForm.reset();
        } catch (error) {
            console.error('Error creating showtime:', error);
            alert('Failed to create showtime. Please try again.');
        }
    }

    async function fetchUsers() {
        try {
            const response = await fetch('http://localhost:8000/users/', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            if (!response.ok) throw new Error('Failed to fetch users');
            const users = await response.json();
            displayUsers(users);
        } catch (error) {
            console.error('Error fetching users:', error);
            usersListElement.innerHTML = '<p>Failed to load users. Please try again later.</p>';
        }
    }

    function displayUsers(users) {
        usersListElement.innerHTML = '<h4>Users</h4>';
        users.forEach(user => {
            const userElement = document.createElement('div');
            userElement.innerHTML = `
                <p>Username: ${user.username}</p>
                <p>Email: ${user.email}</p>
                <p>Role: ${user.role}</p>
                <button onclick="updateUser(${user.id})">Update</button>
                <button onclick="deleteUser(${user.id})">Delete</button>
                <hr>
            `;
            usersListElement.appendChild(userElement);
        });
    }

    

    window.deleteUser = async function(userId) {
        if (confirm('Are you sure you want to delete this user?')) {
            try {
                const response = await fetch(`http://localhost:8000/users/${userId}`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                if (!response.ok) throw new Error('Failed to delete user');
                alert('User deleted successfully!');
                fetchUsers(); // Refresh the user list
            } catch (error) {
                console.error('Error deleting user:', error);
                alert('Failed to delete user. Please try again.');
            }
        }
    }

    function logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('role');
        window.location.href = '/static/index.html';
    }
});