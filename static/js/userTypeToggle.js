document.addEventListener("DOMContentLoaded", function() {
    const dogWalkerRadio = document.getElementById('dog-walker');
    const dogOwnerRadio = document.getElementById('dog-owner');
    const dogWalkerDetails = document.getElementById('dog-walker-details');
    const dogOwnerDetails = document.getElementById('dog-owner-details');

    function toggleDetails() {
        if (dogWalkerRadio.checked) {
            dogWalkerDetails.style.display = 'block';
            dogOwnerDetails.style.display = 'none';
            // Disable all dog owner inputs and enable walker inputs
            toggleInputs(dogOwnerDetails, true);
            toggleInputs(dogWalkerDetails, false);
        } else if (dogOwnerRadio.checked) {
            dogWalkerDetails.style.display = 'none';
            dogOwnerDetails.style.display = 'block';
            // Disable all dog walker inputs and enable owner inputs
            toggleInputs(dogWalkerDetails, true);
            toggleInputs(dogOwnerDetails, false);
        }
    }

    function toggleInputs(section, disable) {
        section.querySelectorAll('input, button').forEach(input => {
            input.disabled = disable;
        });
    }

    toggleDetails();
    dogWalkerRadio.addEventListener('change', toggleDetails);
    dogOwnerRadio.addEventListener('change', toggleDetails);

    const addDogButton = document.getElementById('add-dog-button');
    let dogCount = 2;

    addDogButton.addEventListener('click', function() {
        while (document.getElementById(`dog-name-${dogCount}`)) {
            dogCount++;
        }

        const dogSection = document.createElement('div');
        dogSection.innerHTML = `
            <label class="form-label">Dog ${dogCount}</label>
            <div class="row">
                <div class="col-sm-4">
                  <input type="text" class="form-control" id="dog-name-${dogCount}" placeholder="Name" aria-label="Dog Name" required>
                </div>
                <div class="col-sm-4">
                  <input type="text" class="form-control" id="dog-breed-${dogCount}" placeholder="Breed" aria-label="Dog Breed" required>
                </div>
                <div class="col-sm-2">
                  <input type="number" class="form-control" id="dog-age-${dogCount}" placeholder="Age" aria-label="Dog Age" min="0" max="31" required>
                </div>
                <div class="col-sm-2">
                  <button type="button" id="delete-${dogCount}" class="btn btn-danger">Delete</button>
                </div>
            </div><br>
        `;
        dogOwnerDetails.insertBefore(dogSection, addDogButton);
        // Ensure new fields are disabled based on the current selection
        toggleInputs(dogSection, !dogOwnerRadio.checked);
        dogCount++;

        const deleteButton = dogSection.querySelector(`#delete-${dogCount - 1}`);
        deleteButton.addEventListener('click', function() {
            dogSection.parentNode.removeChild(dogSection);
            dogCount--;
            while (document.getElementById(`dog-name-${dogCount}`) == null && dogCount > 2) {
                dogCount--;
            }
        });
    });
});
