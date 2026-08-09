document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('albumSearch');
    if (searchInput) {
        searchInput.addEventListener('input', function () {
            const filter = this.value.toLowerCase();
            const rows = document.querySelectorAll('table tbody tr');
            rows.forEach(row => {
                const title = row.cells[1].textContent.toLowerCase();
                row.style.display = title.includes(filter) ? '' : 'none';
            });
        });
    }

    const thumbnailInput = document.getElementById('id_thumbnail');
    const preview = document.getElementById('thumbnailPreview');
    if (thumbnailInput && preview) {
        thumbnailInput.addEventListener('change', function () {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                };
                reader.readAsDataURL(file);
            } else {
                preview.src = '#';
                preview.style.display = 'none';
            }
        });
    }
});

function confirmDelete(url) {
    const modal = document.getElementById('deleteModal');
    const form = document.getElementById('deleteForm');
    form.action = url;
    modal.classList.add('active');
}

function closeDeleteModal() {
    const modal = document.getElementById('deleteModal');
    modal.classList.remove('active');
}