const goBtn = document.getElementById("add-recipe");
const input = document.getElementById("recipe-url");
const yield = document.getElementById("servingYield");

// when user searches a recipe
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
        yield.textContent = data.yields;
        write_list(ingredientList, data.ingredients)
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
    groceryModal.addEventListener("shown.bs.modal", async () => {
        const response = await fetch("/grocery-list");
        groceryList.innerHTML = "";
        if (response.status === 200) {
            // create items
            errorMessage.hidden = true;
            const data = await response.json();
            write_list(groceryList, data.items)
        }
        else if (response.status === 204) { // empty list
            errorMessage.hidden = false;
        }
    });
});

const increaseServingBtn = document.getElementById("increaseServing");
increaseServingBtn.addEventListener("click", async () => {
    if (yield.textContent <= 99) {
        let servings = parseInt(yield.textContent) + 1;

        let response = await fetch("/get-recipe");
        const recipe = await response.json();

        let scale = servings / recipe.yields
        fetchRecipe(scale).then(data => {
            const ingredientList = document.getElementById("ingredient-list");
            yield.textContent = data.servings;
            // rewrite ingredient list
            write_list(ingredientList, data.ingredients)
        });
    }
    
});

const decreaseServingBtn = document.getElementById("decreaseServing");
decreaseServingBtn.addEventListener("click", async () => {
    if (yield.textContent > 1) {
        let servings = parseInt(yield.textContent) - 1

        let response = await fetch("/get-recipe");
        const recipe = await response.json();

        let scale = servings / recipe.yields
        fetchRecipe(scale).then(data => {
            const ingredientList = document.getElementById("ingredient-list");
            yield.textContent = data.servings;
            // rewrite ingredient list
            write_list(ingredientList, data.ingredients)
        });
    }
});

const radioBtns = document.querySelectorAll(".btn-group .btn-check");
radioBtns.forEach(btn => {
    btn.addEventListener("change", async () => {
        const checkedBtn = document.querySelector('.btn-group .btn-check:checked');
        const label = document.querySelector(`label[for="${checkedBtn.id}"]`)
       
        const scale = parseFloat(label.textContent.substring(0, label.textContent.length - 1));
        fetchRecipe(scale).then(data => {
            const ingredientList = document.getElementById("ingredient-list");
            yield.textContent = data.servings;
            // rewrite ingredient list
            write_list(ingredientList, data.ingredients)
        });
       
        
    });
});

async function fetchRecipe(scale) {
    const response = await fetch("/scale-recipe", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            multiplier: scale
        })
    });
    const data = await response.json();
    return data;
}

function write_list(element, list, newList = true) {
    // display list of items
    if (newList) {
        element.innerHTML = "";
    }

    for (let i = 0; i < list.length; i++) {
        let row = document.createElement("li");
        row.textContent = list[i];
        element.appendChild(row);
    }
}

const addIngredients = document.getElementById("addIngredients");
addIngredients.addEventListener("click", async () => {
    await fetch("/add-recipe", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }
    });
    document.getElementById("ingredient-container").hidden = true;
})