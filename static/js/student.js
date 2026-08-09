document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('studentSearch');
    if (searchInput) {
        searchInput.addEventListener('input', function () {
            const filter = this.value.toLowerCase();
            const rows = document.querySelectorAll('table tbody tr');
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(filter) ? '' : 'none';
            });
        });
    }
});

function confirmDelete(url) {
    document.getElementById('deleteForm').action = url;
    document.getElementById('deleteModal').classList.add('active');
}

function confirmReset(url) {
    document.getElementById('resetPasswordForm').action = url;
    document.getElementById('resetPasswordModal').classList.add('active');
}

function closeModal(id) {
    document.getElementById(id).classList.remove('active');
}