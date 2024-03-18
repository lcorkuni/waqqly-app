document.addEventListener("DOMContentLoaded", function() {
    // Define variables for the radio buttons
    const dogWalkerRadio = document.getElementById('dog-walker');
    const dogOwnerRadio = document.getElementById('dog-owner');

    // Define variables for the sections
    const dogWalkerDetails = document.getElementById('dog-walker-details');
    const dogOwnerDetails = document.getElementById('dog-owner-details');

    // Function to toggle visibility
    function toggleDetails() {
        if (dogWalkerRadio.checked) {
            dogWalkerDetails.style.display = 'block';
            dogOwnerDetails.style.display = 'none';
        } else if (dogOwnerRadio.checked) {
            dogWalkerDetails.style.display = 'none';
            dogOwnerDetails.style.display = 'block';
        }
    }

    // Initialize visibility based on the default checked radio button
    toggleDetails();

    // Event listeners for change on radio buttons
    dogWalkerRadio.addEventListener('change', toggleDetails);
    dogOwnerRadio.addEventListener('change', toggleDetails);

    // Additional JavaScript for dynamically adding dog fields
    const addDogButton = document.getElementById('add-dog-button');
    let dogCount = 1;

    addDogButton.addEventListener('click', function() {
        const dogSection = document.createElement('div');
        dogSection.innerHTML = `
            <label>Dog ${dogCount}:</label><br>
            <label for="dog-name-${dogCount}">Dog Name:</label>
            <input type="text" id="dog-name-${dogCount}" name="dog-name-${dogCount}"><br>
            <label for="dog-breed-${dogCount}">Dog Breed:</label>
            <input type="text" id="dog-breed-${dogCount}" name="dog-breed-${dogCount}"><br>
            <label for="dog-age-${dogCount}">Dog Age:</label>
            <input type="number" id="dog-age-${dogCount}" name="dog-age-${dogCount}" min="0"><br>
        `;
        dogOwnerDetails.insertBefore(dogSection, addDogButton);
        dogCount++;
    });

});
