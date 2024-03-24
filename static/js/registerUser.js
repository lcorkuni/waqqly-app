document.addEventListener("DOMContentLoaded", function() {
    const registerForm = document.getElementById('registrationForm');
    const registerButton = document.getElementById('register');

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
    registerButton.parentNode.insertBefore(lineBreak, registerButton.nextSibling);
    registerButton.parentNode.insertBefore(spinner, lineBreak.nextSibling);

    // Listen for form submission
    registerForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        const password1 = document.getElementById('inputPassword1').value;
        const password2 = document.getElementById('inputPassword2').value;

        // Check if passwords match
        if (password1 !== password2) {
            alert("Passwords do not match!");
            return;
        }

        // Show spinner
        spinner.classList.remove('invisible');

        // Prepare the form data as JSON
        const formData = {
            email: document.getElementById('inputEmail').value,
            username: document.getElementById('inputUsername').value,
            password: password1, // Assuming backend validation/hashing
            userType: document.getElementById('dog-walker').checked ? 'Dog Walker' : 'Dog Owner',
            details: {} // Placeholder for additional details
        };

        // Add dog owner or walker details based on selection
        if (formData.userType === 'Dog Owner') {
            // Gather dog details
            formData.details.dogs = [...document.querySelectorAll('[id^="dog-name-"]')].map((dogNameElement, index) => ({
                name: dogNameElement.value,
                breed: document.querySelectorAll('[id^="dog-breed-"]')[index].value,
                age: parseInt(document.querySelectorAll('[id^="dog-age-"]')[index].value, 10)
            }));
        } else if (formData.userType === 'Dog Walker') {
            formData.details = {
                firstName: document.querySelector('[aria-label="First name"]').value,
                lastName: document.querySelector('[aria-label="Last name"]').value,
                age: parseInt(document.querySelector('[aria-label="Age"]').value, 10)
            };
        }

        // Send the form data to the /signup endpoint
        fetch('/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            // Hide spinner
            spinner.classList.add('invisible');

            if (!response.ok) {
                throw new Error('Network response was not ok');
            } else {
                alert(`User ${formData.username} successfully registered! Redirecting to login.`);
                window.location.href = '/login';
            }
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
            alert('An error occurred while registering the user.');
            // Hide spinner in case of error
            spinner.classList.add('invisible');
        });
    });
});
