const groceryList = document.getElementById("grocery-list");

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
document.addEventListener("DOMContentLoaded", async () => {
    // detect when modal is about to be shown
    const groceryModal = document.getElementById("groceryListModal");
    groceryModal.addEventListener("shown.bs.modal", async () => {
        const errorMessage = document.querySelector(".modal-body .error-message");
        const response = await fetch("/grocery-list");
        groceryList.innerHTML = "";
        if (response.status === 200) {
            // create items
            errorMessage.hidden = true;
            const data = await response.json();
            write_list(groceryList, data.items, true, true);
        }
        else if (response.status === 204) { // empty list
            errorMessage.hidden = false;
        }
    });
});

function write_list(element, list, newList=true, isGroceryList=false) {
    // display list of items
    if (newList) {
        element.innerHTML = "";
    }
    for (let i = 0; i < list.length; i++) {
        let item = document.createElement("li");
        if (isGroceryList) {
            item.innerHTML = "〇  " + list[i];
        }
        else {
            item.textContent = list[i];
        }
        element.appendChild(item);
    }
}

// cross off items on grocery list
groceryList.addEventListener("click", function(e) {
  if (e.target.tagName === "LI") {
    e.target.classList.toggle("checked");
  }
});

// clear checked items on grocery list
document.getElementById("clearGroceryList").addEventListener("click", () => {
    groceryList.querySelectorAll("li").forEach(item => {
        item.classList.remove("checked");
    })
});

// reset grocery list
document.getElementById("resetGroceryList").addEventListener("click", () => {
    fetch("/reset-grocery-list", { method: "POST" })
        .then(() => {
            const errorMessage = document.querySelector(".modal-body .error-message");
            errorMessage.hidden = false;
            groceryList.querySelectorAll("li").forEach(li => li.remove());
        })
        .catch(err => console.error("Error resetting grocery list:", err));
});

const copyBtn = document.getElementById("copyGroceryList");
copyBtn.addEventListener("click", async () => {
    const response = await fetch("/get-list-as-str");
    const data = await response.json();
    navigator.clipboard.writeText(data.list);
});