document.getElementById('login-form').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent form submission
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                username: username,
                password: password,
            }),
        });

        if (response.ok) {
            window.location.href = '/home';
        } else {
            const errorMessage = "No user found"; // Update to a more generic error message if necessary
            document.getElementById('error-message').innerText = errorMessage;
            document.getElementById('error-message').style.display = 'block';
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('error-message').innerText = 'An unexpected error occurred.';
        document.getElementById('error-message').style.display = 'block';
    }
});
