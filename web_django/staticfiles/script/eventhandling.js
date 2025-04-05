document.addEventListener("DOMContentLoaded", function () {
    // Mouseout Event
    document.querySelectorAll(".about").forEach(function (element) {
        element.addEventListener("mouseout", function () {
            this.style.backgroundColor = "#f8f8f8"; // Change background color on mouse out
        });
    });

    // Focus Event (for input fields)
    document.querySelectorAll("input, textarea").forEach(function (element) {
        element.addEventListener("focus", function () {
            this.style.border = "2px solid blue"; // Highlight input on focus
        });
        element.addEventListener("blur", function () {
            this.style.border = ""; // Remove border when focus is lost
        });
    });

    // Hover Event
    document.querySelectorAll(".menu li a").forEach(function (element) {
        element.addEventListener("mouseover", function () {
            this.style.color = "red"; // Change text color on hover
        });
        element.addEventListener("mouseout", function () {
            this.style.color = ""; // Reset color on mouse out
        });
    });

    // Disable Right-Click
    document.addEventListener("contextmenu", function (event) {
        event.preventDefault();
        alert("Right-click is disabled on this page!");
    });

    // Click Event for the Video Section
    // document.querySelector(".video-section").addEventListener("click", function () {
    //     alert("You clicked on the video section!");
    // });
});
