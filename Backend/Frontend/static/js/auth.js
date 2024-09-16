// Login Form
document.getElementById('login-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const response = await fetch('http://localhost:8000/token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
    });

    if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('role', data.role);
        
        if (data.role === 'Admin') {
            window.location.href = '/static/admin.html';
        } else {
            window.location.href = '/static/user.html';
        }
    } else {
        alert('Login failed!');
    }
});

// Registration Form
document.getElementById('register-form').addEventListener('submit', async function(e) {
    e.preventDefault();  // Prevent the default form submission

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const email = document.getElementById('email').value;
    const role = document.getElementById('role').value;

    try {
        const response = await fetch('http://127.0.0.1:8000/users/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'  // Ensure the content type is JSON
            },
            body: JSON.stringify({ username, password, email, role })  // Send data in the body as JSON
        });

        if (response.ok) {
            const data = await response.json();
            alert(data.message);  // Display success message
            window.location.href = '/static/index.html';  // Redirect to login
        } else {
            const errorData = await response.json();
            alert(`Error: ${errorData.detail}`);  // Display error message
        }
    } catch (error) {
        console.error('Error during registration:', error);
        alert('An error occurred during registration.');
    }
});
