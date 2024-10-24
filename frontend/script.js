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
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    // Send login request to the backend
    const response = await fetch('/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },  // Use URL-encoded format for login
        body: new URLSearchParams({ email, password })
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

// document.addEventListener('DOMContentLoaded', () => {
//     const loginButton = document.getElementById('login-button');  // Target by button id
    
//     if (loginButton) {
//         loginButton.addEventListener('click', async function(event) {
//             event.preventDefault();  // Prevent the form from submitting the old way
//             console.log('Login button clicked');  // Debugging message to verify click

//             const email = document.getElementById('email').value;
//             const password = document.getElementById('password').value;

//             // Send login request to backend
//             try {
//                 const response = await fetch('/auth/login', {
//                     method: 'POST',
//                     headers: { 'Content-Type': 'application/json' },
//                     body: JSON.stringify({ email, password })  // Include form data in request
//                 });

//                 if (response.ok) {
//                     const data = await response.json();
//                     localStorage.setItem('token', data.access_token);  // Save token
//                     alert('Login successful!');
//                     window.location.href = '/static/home_logged_in.html';  // Redirect to logged-in page
//                 } else {
//                     alert('Login failed. Please check your credentials.');
//                 }
//             } catch (error) {
//                 console.error('Error during login:', error);
//             }
//         });
//     } else {
//         console.error('Login button not found');
//     }
// });



// Log Out Button Handler
document.getElementById('logout-button')?.addEventListener('click', function() {
    localStorage.removeItem('token');  // Remove token on logout
    window.location.href = '/static/index.html';  // Redirect to the non-logged-in home page
});


// For Communities Page
document.addEventListener("DOMContentLoaded", async () => {
    // Check if the current URL matches the communities.html page
    if (window.location.pathname === "/static/communities.html") {
        try {
            const response = await fetch("/communities/");
            
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            
            const communities = await response.json();
            console.log(communities); // Log the communities for debugging

            // HTML for communities.html
            const container = document.getElementById("communities-container");
            communities.forEach(community => {
                const communityCard = document.createElement("div");
                communityCard.classList.add("community-card");

                communityCard.innerHTML = `
                    <img src="${community.image_url}" alt="${community.name}" />
                    <h2>${community.name}</h2>
                    <p>${community.description}</p>
                    <p>Members: ${community.members_count}</p>
                    <button onclick="joinCommunity('${community._id}')">Join</button>
                `;

                container.appendChild(communityCard);
            });
        } catch (error) {
            console.error('Error fetching communities:', error);
        }
    }
});




// Example joinCommunity function
function joinCommunity(communityId) {
    // Logic to join the community
    alert(`Joining community with ID: ${communityId}`);
}

// For emotions
// Emotion Log Form Handler
document.getElementById('emotion-form')?.addEventListener('submit', async function(event) {
    event.preventDefault();  // Prevent the default form submission behavior
    localStorage.setItem('token', data.access_token);  // Save the token in localStorage

    // Collect form data
    const mood = document.getElementById('mood').value;
    const stress = document.getElementById('stress').value;

    // Create an object with the collected data
    const emotionData = {
        mood_level: parseInt(mood),  // Convert to integer
        stress_level: parseInt(stress)  // Convert to integer
    };

    try {
        // Send log emotion request to the backend
        const response = await fetch('/emotion-tracking', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`  // Include JWT token
            },
            body: JSON.stringify(emotionData)
        });

        if (response.ok) {
            const result = await response.json();
            alert(`Emotion logged successfully! ID: ${result.id}`);
        } else {
            const errorData = await response.json();
            alert(`Failed to log emotion: ${errorData.detail}`);
        }
    } catch (error) {
        console.error('Error during emotion logging:', error);
        alert('An error occurred while logging emotion. Please try again later.');
    }
});