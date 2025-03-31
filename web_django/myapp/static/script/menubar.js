document.addEventListener("DOMContentLoaded", function () {
    // Create menu container
    const menuContainer = document.createElement("div");
    menuContainer.classList.add("menu-container");
    
    // Create menu button
    const menuButton = document.createElement("button");
    menuButton.classList.add("menu-button");
    menuButton.innerHTML = "&#9776;"; // Unicode for hamburger icon
    
    // Create menu list
    const menuList = document.createElement("ul");
    menuList.classList.add("menu-list");
    menuList.style.display = "none"; // Initially hidden
    
    // Define menu items
    const menuItems = [
        { text: "FAQ", link: "faqs" },
        { text: "About Us", link: "about" },
        { text: "Contact", link: "contact" }
    ];
    
    // Populate menu
    menuItems.forEach(item => {
        const listItem = document.createElement("li");
        const anchor = document.createElement("a");
        anchor.href = item.link;
        anchor.textContent = item.text;
        listItem.appendChild(anchor);
        menuList.appendChild(listItem);
    });
    
    // Append elements
    menuContainer.appendChild(menuButton);
    menuContainer.appendChild(menuList);
    document.querySelector("header").prepend(menuContainer);
    
    // Toggle menu visibility and position below button
    menuButton.addEventListener("click", function () {
        event.stopPropagation(); 
        if (menuList.style.display === "none" || menuList.style.display === "") {
            menuList.style.display = "block";
            menuList.style.position = "fixed";
            menuList.style.top = "50px"; // Positioning below the button
            menuList.style.right = "10px";
            menuList.style.background = "white";
            menuList.style.padding = "10px";
            menuList.style.boxShadow = "0px 4px 6px rgba(0, 0, 0, 0.1)";
        } else {
            menuList.style.display = "none";
        }
    });
    
    // Make the button fixed at the top left corner
    menuButton.style.position = "fixed";
    menuButton.style.top = "10px";
    menuButton.style.left = "10px";
    menuButton.style.zIndex = "1000";
    
    // Show button when scrolling up, but only show menu when clicked
    let lastScrollTop = 0;
    window.addEventListener("scroll", function () {
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        if (scrollTop < lastScrollTop) {
            menuButton.style.display = "block";
        }
        lastScrollTop = scrollTop;
    });
});
