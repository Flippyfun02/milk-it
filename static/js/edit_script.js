const addIngredientBtn = document.getElementById("addIngredients");
addIngredientBtn.addEventListener("click", async () => {
    const ingredients = document.getElementById("customIngredients");
    const response = await fetch("/add-ingredients", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            ingredients_list: ingredients.value
        })
    });
    ingredients.value = "";
});