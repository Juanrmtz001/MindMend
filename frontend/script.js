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



document.getElementById('login-form')?.addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch('/auth/login', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({
                username: email,  // OAuth2 expects 'username' field
                password: password
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('token', data.access_token);
            window.location.href = '/static/home_logged_in.html';
        } else {
            const errorData = await response.json();
            alert(errorData.detail || 'Login failed. Please check your credentials.');
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('An error occurred during login. Please try again.');
    }
});


// Log Out Button Handler
document.getElementById('logout-button')?.addEventListener('click', function() {
    localStorage.removeItem('token');  // Remove token on logout
    window.location.href = '/';  // Redirect to the non-logged-in home page
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
// document.getElementById('emotion-form')?.addEventListener('submit', async function(event) {
//     event.preventDefault();  // Prevent the default form submission behavior
//     localStorage.setItem('token', data.access_token);  // Save the token in localStorage

//     // Collect form data
//     const mood = document.getElementById('mood').value;
//     const stress = document.getElementById('stress').value;

//     const emotionData = {
//         mood_level: parseInt(mood),
//         stress_level: parseInt(stress)
//     };
    
//     try {
//         const response = await fetch('/emotion-tracking/', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'Authorization': `Bearer ${localStorage.getItem('token')}`
//             },
//             body: JSON.stringify(emotionData)
//         });

//         if (response.ok) {
//             const result = await response.json();
//             alert(`Emotion logged successfully! ID: ${result.id}`);
//         } else {
//             const errorData = await response.json();
//             alert(`Failed to log emotion: ${errorData.detail}`);
//         }
//     } catch (error) {
//         console.error('Error during emotion logging:', error);
//         alert('An error occurred while logging emotion. Please try again later.');
//     }
// });


// Function to log emotions
async function logEmotion(mood, stress) {
    try {
        const response = await fetch('/emotion-tracking/emotions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${yourAuthToken}` // Make sure you have the auth token
            },
            body: JSON.stringify({
                mood: parseInt(mood),
                stress: parseInt(stress)
            })
        });

        if (!response.ok) {
            const errorData = await response.text();
            throw new Error(errorData);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error logging emotion:', error);
        throw error;
    }
}

// Example usage
// logEmotion(7, 4)
//     .then(response => console.log('Success:', response))
//     .catch(error => console.error('Error:', error));