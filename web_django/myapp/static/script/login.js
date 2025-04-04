async function validateLoginForm(event) {
    // get the form data
    // event.preventDefault(); // Prevent the default form submission
    const form = event.target;
    const username = form["email"].value;
    const password = form["password"].value;

    console.log(username, password);

    try {
        const response = await fetch('https://web-project-lbcv.onrender.com/auth/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Login failed. Please check your credentials.');
        }

        const data = await response.json();
        console.log('Login successful:', data);

        // Store the token in localStorage
        localStorage.setItem('authToken', data.token);

        // Optionally store user details
        localStorage.setItem('username', data.username);
        localStorage.setItem('userId', data.user_id);

        // Redirect to a dashboard or home page
        window.location.href = '/dashboard/';
    } catch (error) {
        console.error('Error during login:', error);
        alert(error.message);
    }
}