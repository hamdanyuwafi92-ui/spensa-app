function openModal(modalId, actionUrl) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        if (actionUrl) {
            const form = modal.querySelector('form');
            if (form) form.action = actionUrl;
        }
    }
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

function editClub(id, code, name) {
    openModal('modalClubForm', '/core/club/' + id + '/update/');
    document.getElementById('modalClubTitle').textContent = 'Edit Ekstrakurikuler';
    document.getElementById('clubCode').value = code;
    document.getElementById('clubName').value = name;
}

function confirmDeleteClub(url) {
    document.getElementById('deleteClubForm').action = url;
    openModal('deleteClubModal');
}