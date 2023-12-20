const answerForm = document.getElementById('answer-form');
const imageInput = document.getElementById('image');
const imagePreview = document.getElementById('image-preview');
const feedbackMessage = document.getElementById('feedback-message');
const submitButton = document.getElementById('submit-button'); // Submit button
const loginPrompt = document.getElementById('login-prompt'); // Sign-in prompt

// Handle file input change to show image preview
imageInput.addEventListener('change', () => {
    const file = imageInput.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            imagePreview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
});


// Simulated user authentication (replace with your actual authentication logic)
const isAuthenticated = false; // Change to true if the user is authenticated

if (!isAuthenticated) {
    // If not authenticated, apply blur effect and show sign-in prompt
    answerForm.classList.add('blur');
    submitButton.disabled = true;
    loginPrompt.style.display = 'block';
}

// Handle form submission (for authenticated users only)
answerForm.addEventListener('submit', (e) => {
    e.preventDefault();

    // Simulate form submission (replace with your actual submission logic)
    setTimeout(() => {
        feedbackMessage.textContent = 'Answer submitted successfully!';
        feedbackMessage.classList.add('text-success');
        // Clear the form
        answerForm.reset();
        imagePreview.style.display = 'none';
    }, 2000); // Simulated delay for demonstration
});