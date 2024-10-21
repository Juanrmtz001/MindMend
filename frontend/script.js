document.addEventListener('DOMContentLoaded', () => {
    console.log('Welcome to MindMend!');
});

// Sign Up Form Handler
document.getElementById('signup-form')?.addEventListener('submit', async function(event) {
    event.preventDefault();  // Prevent the default form submission behavior
    
    // Collect form data
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Assuming the backend requires a name and birthday as well, add these here (you can customize)
    const name = 'Test User';  // You can modify this to collect from the user
    const birthday = '1990-01-01T00:00:00';  // Fixed birthday for now

    try {
        // Send sign-up request to the backend
        const response = await fetch('/auth/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                username, 
                email, 
                password, 
                name,
                birthday  // Ensure all required fields are included
            })
        });

        if (response.ok) {
            alert('Sign-up successful!');
            window.location.href = '/static/login.html';  // Redirect to login page after successful sign-up
        } else {
            const errorData = await response.json();
            alert(`Sign-up failed: ${errorData.detail}`);
        }
    } catch (error) {
        alert('An error occurred during sign-up. Please try again later.');
    }
});


// Log In Form Handler
document.getElementById('login-form')?.addEventListener('submit', async function(event) {
    event.preventDefault();  // Prevent the default form submission behavior
    
    // Collect form data
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    // Send login request to the backend
    const response = await fetch('/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },  // Use URL-encoded format for login
        body: new URLSearchParams({ username, password })
    });

    if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.access_token);  // Save the token in localStorage

        alert('Login successful!');
        window.location.href = '/static/home_logged_in.html';  // Redirect to the logged-in home page
    } else {
        alert('Login failed. Please check your credentials and try again.');
    }
});

// Log Out Button Handler
document.getElementById('logout-button')?.addEventListener('click', function() {
    localStorage.removeItem('token');  // Remove token on logout
    window.location.href = '/static/index.html';  // Redirect to the non-logged-in home page
});