function openEditModal() {
    document.getElementById('edit-modal').style.display = 'block';
}

function closeEditModal() {
    document.getElementById('edit-modal').style.display = 'none';
}

async function submitEditForm(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);

    try {
        const response = await fetch('/api/edit-news/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: formData
        });

        const result = await response.json();

        if (response.ok && result.success) {
            // Обновляем текст
            document.getElementById('content-text').innerHTML = formData.get('content').replace(/\n/g, '<br>');

            // Обновляем заголовок
            document.querySelector('.display-5').innerText = formData.get('title');

            // Если загружено новое фото — обновляем превью
            const imageFile = formData.get('image');
            if (imageFile) {
                let imgElement = document.getElementById('image-preview');
                if (!imgElement) {
                    // Если фото не было — создаём
                    const container = document.querySelector('.mb-4');
                    if (container) {
                        container.innerHTML = `<img id="image-preview" class="img-fluid rounded shadow-sm" alt="Новость">`;
                        imgElement = document.getElementById('image-preview');
                    }
                }
                if (imgElement) {
                    imgElement.src = URL.createObjectURL(imageFile);
                }
            }

            // Если отмечено удаление — удаляем превью
            if (formData.get('delete_image') === 'on') {
                const imgElement = document.getElementById('image-preview');
                if (imgElement) {
                    imgElement.remove();
                    const container = document.querySelector('.mb-4');
                    if (container) {
                        container.innerHTML = `<div class="alert alert-warning">Фото удалено.</div>`;
                    }
                }
            }

            alert('Новость обновлена!');
            closeEditModal();
        } else {
            alert('Ошибка: ' + (result.error || 'Неизвестная ошибка'));
        }
    } catch (err) {
        console.error(err);
        alert('Произошла ошибка при сохранении.');
    }
}

// Привязываем обработчик к форме при загрузке страницы
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('edit-news-form');
    if (form) {
        form.addEventListener('submit', submitEditForm);
    }
});