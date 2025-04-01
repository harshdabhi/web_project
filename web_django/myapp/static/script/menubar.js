document.addEventListener("DOMContentLoaded", function () {
    // Create menu container
    const menuContainer = document.createElement("div");
    menuContainer.classList.add("menu-container");
    menuContainer.style.position = "relative";
    // Create menu button
    const menuButton = document.createElement("button");
    menuButton.classList.add("menu-button");
    menuButton.innerHTML = "&#9776;"; // Unicode for hamburger icon
    menuButton.style.position = "absolute";
    menuButton.style.top = "10px";
    menuButton.style.right = "10px";
    menuButton.style.zIndex = "1000";
    
    // Create menu list
    const menuList = document.createElement("ul");
    menuList.classList.add("menu-list");
    menuList.style.display = "none"; // Initially hidden
    menuList.style.position = "absolute";
    menuList.style.top = "40px";
    menuList.style.right = "10px";
    menuList.style.background = "white";
    menuList.style.padding = "10px";
    menuList.style.boxShadow = "0px 4px 6px rgba(0, 0, 0, 0.1)";

    
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
    document.querySelector("header").appendChild(menuContainer);
    
    // Toggle menu visibility and position below button
    menuButton.addEventListener("click", function (event) {
        event.stopPropagation(); 
        menuList.style.display = menuList.style.display === "block" ? "none" : "block";
    });
    
    document.addEventListener("click", function () {
        menuList.style.display = "none";
    });
    menuList.addEventListener("click", function (event) {
        event.stopPropagation();
    });
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
