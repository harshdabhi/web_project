document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("login-form").addEventListener("submit", function (event) {
        let isValid = true;
        
        // Get form fields
        const emailField = document.getElementById("email");
        const passwordField = document.getElementById("password");
        
        // Remove previous error messages
        document.querySelectorAll(".error-message").forEach(e => e.remove());

        // Email validation
        if (!emailField.value.trim()) {
            showError(emailField, "Email is required.");
            isValid = false;
        }

        // Password validation (must contain uppercase, lowercase, special character, and be exactly 10 characters)
        const password = passwordField.value;
        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{10}$/;
        
        if (!passwordRegex.test(password)) {
            showError(passwordField, "Password must be 10 characters long and include uppercase, lowercase, and a special character.");
            isValid = false;
        }
        
        // Prevent form submission if validation fails
        if (!isValid) {
            event.preventDefault();
        }
    });

    function showError(inputElement, message) {
        const errorElement = document.createElement("p");
        errorElement.className = "error-message";
        errorElement.style.color = "red";
        errorElement.style.fontSize = "0.9rem";
        errorElement.textContent = message;
        inputElement.insertAdjacentElement("afterend", errorElement);
    }
});
