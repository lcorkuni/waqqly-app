document.getElementById("sign-out-btn").addEventListener("click", async () => {
    try {
        const response = await fetch("/del_cookie", {
            method: "GET",
            credentials: "same-origin"
        });
        if (response.ok) {
            window.location.href = "/login";
        } else {
            console.error("Failed to delete cookie");
        }
    } catch (error) {
        console.error("Error occurred while signing out:", error);
    }
});
