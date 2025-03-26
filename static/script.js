document.addEventListener("DOMContentLoaded", function () {
    console.log("JS Loaded!");

    // Add to Cart
    document.querySelectorAll(".add-to-cart").forEach(button => {
        button.addEventListener("click", function () {
            let name = this.dataset.name;
            let price = parseFloat(this.dataset.price);

            fetch("/add_to_cart", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name, price })
            })
            .then(response => response.json())
            .then(data => alert(data.message));
        });
    });

    // Remove from Cart
    document.querySelectorAll(".remove-item").forEach(button => {
        button.addEventListener("click", function () {
            let name = this.dataset.name;

            fetch("/remove_from_cart", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name })
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                location.reload();
            });
        });
    });

    // Search Functionality
    document.querySelector("#search-input")?.addEventListener("keyup", function () {
        let query = this.value.toLowerCase();
        document.querySelectorAll(".book").forEach(book => {
            let title = book.querySelector("h3").innerText.toLowerCase();
            book.style.display = title.includes(query) ? "block" : "none";
        });
    });
});
