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
            <label class="form-label">Dog ${dogCount}</label>
            <div class="row">
                <div class="col-sm-4">
                  <input type="text" class="form-control" id="dog-name-${dogCount}" placeholder="Name" aria-label="Dog Name">
                </div>
                <div class="col-sm-4">
                  <input type="text" class="form-control" id="dog-breed-${dogCount}" placeholder="Breed" aria-label="Dog Breed">
                </div>
                <div class="col-sm-2">
                  <input type="number" class="form-control" id="dog-age-${dogCount}" placeholder="Age" aria-label="Dog Age" min="0" max="31">
                </div>
                <div class="col-sm-2">
                  <button type="button" id="delete-${dogCount}" class="btn btn-danger">Delete</button>
                </div>
            </div><br>
        `;
        dogOwnerDetails.insertBefore(dogSection, addDogButton);
        dogCount++;

        // Attach event listener for delete button
        const deleteButton = dogSection.querySelector(`#delete-${dogCount - 1}`);
        deleteButton.addEventListener('click', function() {
            // Remove the parent row element
            dogSection.parentNode.removeChild(dogSection);
        });
    });
});
