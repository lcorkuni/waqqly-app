document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.getElementById('login-form');
    const loginButton = document.getElementById('login');

    // Create spinner element
    const spinner = document.createElement('div');
    spinner.classList.add('d-flex', 'flex-column', 'align-items-center', 'text-success');
    const innerSpinner = document.createElement('div');
    innerSpinner.classList.add('spinner-border');
    innerSpinner.setAttribute('role', 'status');
    const visuallyHiddenText = document.createElement('span');
    visuallyHiddenText.classList.add('visually-hidden');
    visuallyHiddenText.innerText = 'Loading...';

    // Append elements
    innerSpinner.appendChild(visuallyHiddenText);
    spinner.appendChild(innerSpinner);

    // Initially hide spinner
    spinner.classList.add('invisible');

    // Create and insert <br> before the spinner
    const lineBreak = document.createElement('br');
    loginButton.parentNode.insertBefore(lineBreak, loginButton.nextSibling);
    loginButton.parentNode.insertBefore(spinner, lineBreak.nextSibling);

    // Listen for form submission
    loginForm.addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevent the default form submission

        // Show spinner
        spinner.classList.remove('invisible');

        // Get username and password
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        try {
            // Send login request
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

            // Hide spinner
            spinner.classList.add('invisible');

            if (response.ok) {
                // Redirect to home page on successful login
                window.location.href = '/home';
            } else {
                // Display error message if login fails
                document.getElementById('error-message').innerText = "No user found";
                document.getElementById('error-message').style.display = 'block';
            }
        } catch (error) {
            console.error('Error:', error);
            // Display error message if an unexpected error occurs
            document.getElementById('error-message').innerText = 'Login Failed';
            document.getElementById('error-message').style.display = 'block';

            // Hide spinner in case of error
            spinner.classList.add('invisible');
        }
    });
});
