// // Authentication Helper Functions
//
// // Check if user is authenticated
// function isAuthenticated() {
//     const token = localStorage.getItem('firebase_token');
//     const userData = localStorage.getItem('user_data');
//     return token && userData;
// }
//
// // Get current user data
// function getCurrentUser() {
//     const userData = localStorage.getItem('user_data');
//     return userData ? JSON.parse(userData) : null;
// }
//
// // Get Firebase token
// function getAuthToken() {
//     return localStorage.getItem('firebase_token');
// }
//
// // Logout function
// async function logout() {
//     try {
//         await firebase.auth().signOut();
//         localStorage.removeItem('firebase_token');
//         localStorage.removeItem('user_data');
//         window.location.href = '/login';
//     } catch (error) {
//         console.error('Logout error:', error);
//         alert('Error logging out. Please try again.');
//     }
// }
//
// // Redirect to login if not authenticated
// function requireAuth() {
//     if (!isAuthenticated()) {
//         window.location.href = '/login';
//         return false;
//     }
//     return true;
// }
//
// // Display user info in navbar
// function displayUserInfo() {
//     const user = getCurrentUser();
//     if (user) {
//         const userDisplayElement = document.getElementById('userDisplayName');
//         if (userDisplayElement) {
//             userDisplayElement.textContent = user.full_name || user.username;
//         }
//     }
// }
//
// // Check authentication on page load
// document.addEventListener('DOMContentLoaded', () => {
//     // Pages that don't require authentication
//     const publicPages = ['/login', '/register'];
//     const currentPath = window.location.pathname;
//
//     if (!publicPages.includes(currentPath)) {
//         requireAuth();
//         displayUserInfo();
//     }
// });
//
// // Refresh token periodically (every 50 minutes)
// setInterval(async () => {
//     try {
//         const user = firebase.auth().currentUser;
//         if (user) {
//             const token = await user.getIdToken(true);
//             localStorage.setItem('firebase_token', token);
//         }
//     } catch (error) {
//         console.error('Token refresh error:', error);
//     }
// }, 50 * 60 * 1000);

// Authentication Helper Functions

// Check if user is authenticated
function isAuthenticated() {
    const token = localStorage.getItem('firebase_token');
    const userData = localStorage.getItem('user_data');
    return token && userData;
}

// Get current user data
function getCurrentUser() {
    const userData = localStorage.getItem('user_data');
    return userData ? JSON.parse(userData) : null;
}

// Get Firebase token
function getAuthToken() {
    return localStorage.getItem('firebase_token');
}

// Logout function
async function logout() {
    try {
        await firebase.auth().signOut();
        localStorage.removeItem('firebase_token');
        localStorage.removeItem('user_data');
        window.location.href = '/login';
    } catch (error) {
        console.error('Logout error:', error);
        alert('Error logging out. Please try again.');
    }
}

// Redirect to login if not authenticated
function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = '/login';
        return false;
    }
    return true;
}

// Display user info in navbar
function displayUserInfo() {
    const user = getCurrentUser();
    if (user) {
        const userDisplayElement = document.getElementById('userDisplayName');
        if (userDisplayElement) {
            userDisplayElement.textContent = user.full_name || user.username;
        }
    }
}

// Check authentication on page load
document.addEventListener('DOMContentLoaded', () => {
    // Pages that don't require authentication
    const publicPages = ['/login', '/register', '/test-firebase'];
    const currentPath = window.location.pathname;

    // Only check auth on protected pages
    if (!publicPages.includes(currentPath)) {
        if (!isAuthenticated()) {
            console.log('Not authenticated, redirecting to login...');
            window.location.href = '/login';
            return;
        }
        displayUserInfo();
    }
});

// Refresh token periodically (every 50 minutes)
setInterval(async () => {
    try {
        const user = firebase.auth().currentUser;
        if (user) {
            const token = await user.getIdToken(true);
            localStorage.setItem('firebase_token', token);
            console.log('Token refreshed');
        }
    } catch (error) {
        console.error('Token refresh error:', error);
    }
}, 50 * 60 * 1000);