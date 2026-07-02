document.addEventListener('click', async (event) => {
    const button = event.target.closest('.toggle-item');
    if (!button) return;

    const groceryId = button.dataset.grocery;
    const itemId = button.dataset.item;
    const url = `/api/groceries/${groceryId}/items/${itemId}/toggle/`;
    const csrftoken = Cookies.get('csrftoken');

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            console.error('Toggle failed');
            return;
        }

        const data = await response.json();

        const itemName = button.closest('li')?.querySelector('.item-name');
        if (!itemName) return;

        if (data.on_hand) {
            button.textContent = "Undo";
            itemName.classList.add('bought');
        } else {
            button.textContent = "Bought";
            itemName.classList.remove('bought');
        }

    } catch (error) {
        console.error('Network error:', error);
    }
});