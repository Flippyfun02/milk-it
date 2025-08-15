const goBtn = document.getElementById("add-recipe");
const input = document.getElementById("recipe-url");
const yield = document.getElementById("servingYield");
let originalYield = 1;

// when user adds recipe
goBtn.addEventListener("click", async () => {
    const recipe_url = document.getElementById("recipe-url")
    let url = recipe_url.value;

    // send POST request to FastAPI
    const response = await fetch("/search-recipe", {
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
    input_error.textContent = " ";

    // validate data
    if (response.status === 400) {
        input_error.textContent = "Please enter a recipe link!"
    }
    else if (response.status === 404) {
        input_error.textContent = "Unable to find recipe :("
    }
    else if (response.status === 200) {
        // reveal ingredient container
        document.getElementById("ingredient-container").hidden = false;
        const ingredientList = document.getElementById("ingredient-list");
        originalYield = parseInt(data.yields);
        yield.textContent = originalYield;
        ingredientList.innerHTML = "";
        // display list of items
        for (index in data.ingredients) {
            let row = document.createElement("li");
            row.textContent = data.ingredients[index];
            ingredientList.appendChild(row);
        }
        // ingredients.textContent = JSON.stringify(data.ingredients);
        recipe_url.value = "";
        input_error.textContent = " ";
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

// change button colors between white and green
const listBtn = document.getElementById("open-modal");
const greenSections = document.querySelectorAll(".green-bg");
const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            listBtn.classList.remove("btn-primary")
            listBtn.classList.add("btn-primary-reverse");
        }
        else {
            listBtn.classList.remove("btn-primary-reverse")
            listBtn.classList.add("btn-primary")
        }
    });
}, {
    threshold: 0.1
});

greenSections.forEach(section => observer.observe(section));

// display grocery list
document.addEventListener("DOMContentLoaded", () => {
    const groceryList = document.getElementById("grocery-list");
    const errorMessage = document.querySelector(".modal-body .error-message");
    // detect when modal is about to be shown
    const groceryModal = document.getElementById("groceryListModal");
    groceryModal.addEventListener("show.bs.modal", async () => {
        const response = await fetch("/grocery-list");
        groceryList.innerHTML = "";
        if (response.status === 200) {
            // create items
            errorMessage.hidden = true;
            const data = await response.json();
            for (index in data.ingredients) {
                let row = document.createElement("li");
                row.textContent = data.ingredients[index];
                groceryList.appendChild(row);
            }
        }
        else if (response.status === 204) { // empty list
            errorMessage.hidden = false;
        }
    });
});

const increaseServingBtn = document.getElementById("increaseServing");
increaseServingBtn.addEventListener("click", () => {
    if (yield.textContent <= 99) {
        yield.textContent = parseInt(yield.textContent) + 1
    }
});

const decreaseServingBtn = document.getElementById("decreaseServing");
decreaseServingBtn.addEventListener("click", () => {
    if (yield.textContent > 1) {
        yield.textContent = parseInt(yield.textContent) - 1
    }
});

const radioBtns = document.querySelectorAll(".btn-group .btn-check");
radioBtns.forEach(btn => {
    btn.addEventListener("change", () => {
        const checkedBtn = document.querySelector('.btn-group .btn-check:checked');
        const label = document.querySelector(`label[for="${checkedBtn.id}"]`)
        const scale = parseFloat(label.textContent.substring(0, label.textContent.length - 1));
        yield.textContent = originalYield * scale;
    });
});