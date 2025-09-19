function toggleEditForm(newsId) {
    const form = document.getElementById('edit-form-' + newsId);
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
}

async function submitEditForm(event, newsId) {
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
            // Обновляем DOM без перезагрузки
            document.getElementById('title-' + newsId).innerText = formData.get('title');
            document.getElementById('content-' + newsId).innerText = formData.get('content').substring(0, 200) + '...';

            // Если загружено новое изображение — обновляем его
            const imageFile = formData.get('image');
            if (imageFile) {
                const imgElement = document.getElementById('image-' + newsId);
                if (imgElement && imgElement.tagName === 'IMG') {
                    imgElement.src = URL.createObjectURL(imageFile);
                }
            }

            // Если отмечено удаление — заменяем на заглушку
            if (formData.get('delete_image') === 'on') {
                const imgElement = document.getElementById('image-' + newsId);
                if (imgElement && imgElement.tagName === 'IMG') {
                    imgElement.parentElement.innerHTML = `
                        <div class="card-img-top bg-light d-flex align-items-center justify-content-center"
                             style="height: 200px; width: 100%; border-radius: 0.5rem; margin: 0 auto; padding: 0.5rem;">
                            <span class="text-muted">Изображение отсутствует</span>
                        </div>`;
                }
            }

            toggleEditForm(newsId); // Скрываем форму
            alert('Новость успешно обновлена!');
        } else {
            alert('Ошибка: ' + (result.error || 'Неизвестная ошибка'));
        }
    } catch (err) {
        console.error('Ошибка:', err);
        alert('Произошла ошибка при отправке данных.');
    }
}