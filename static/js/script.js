const goBtn = document.getElementById("add-recipe");
const input = document.getElementById("recipe-url");

goBtn.addEventListener("click", async () => {
    if (input === document.activeElement) {
        const recipe_url = document.getElementById("recipe-url")
        let url = recipe_url.value;

        // send POST request to FastAPI
        const response = await fetch("/add-recipe", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                recipe_url: url
            })
        });
        const data = await response.json();
        const input_error = document.getElementById("input-error")
        input_error.textContent = ""

        if (data.code === 2) {
            input_error.textContent = "Please enter a recipe link!"
        }
        else if (data.code === 3) {
            input_error.textContent = "Unable to find recipe :("
        }
        else {
            ingredients = document.getElementById("ingredients");
            ingredients.textContent = JSON.stringify(data.items);
            recipe_url.value = "";
        }
    }
});

document.addEventListener("keydown", (e) => {
    if (e.key == "Enter" && input === document.activeElement) {
        goBtn.classList.add("press"); // Simulate button click
        goBtn.click();
    }
});

document.addEventListener("keyup", (e) => {
    if (e.key == "Enter") {
        goBtn.classList.remove("press"); // Simulate button click
    }
});