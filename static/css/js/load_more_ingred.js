const loadMoreButton = document.getElementById('load-more-button');
const ingredientsBlock = document.getElementById('ingredients-block');
let offset = 5;

loadMoreButton.addEventListener('click', () => {
    fetch(`/load_more_ingredients/${dishId}/${offset}/`)
        .then(response => response.json())
        .then(data => {
            if (data.length > 0) {
                data.forEach(ingredient => {
                    const checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.name = 'ingredients';
                    checkbox.value = ingredient.id;

                    const label = document.createElement('label');
                    label.textContent = ingredient.name;

                    ingredientsBlock.appendChild(checkbox);
                    ingredientsBlock.appendChild(label);
                });

                offset += 5;
            } else {
                // No more ingredients to load, hide the load more button or handle accordingly
                loadMoreButton.style.display = 'none';
            }
        })
        .catch(error => console.error('Error:', error));
});
