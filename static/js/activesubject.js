function openModal(modalId, actionUrl) {
    var modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        var form = modal.querySelector('form');
        if (form && actionUrl) {
            form.action = actionUrl;
        }
    }
}

function closeModal(modalId) {
    var modal = document.getElementById(modalId);
    if (modal) modal.classList.remove('active');
}

function editActiveSubject(id, activeyear_id, subject_id, classroom_id, teacher_id) {
    openModal('modalActiveSubjectForm', '/core/activesubject/' + id + '/update/');
    document.getElementById('modalActiveSubjectTitle').textContent = 'Edit Mapel Aktif';
    document.getElementById('id_activeyear').value = activeyear_id;
    document.getElementById('id_subject').value = subject_id;
    document.getElementById('id_classroom').value = classroom_id;
    if (teacher_id && teacher_id !== "null") {
        document.getElementById('id_teacher').value = teacher_id;
    } else {
        document.getElementById('id_teacher').value = "";
    }
}

function confirmDelete(url) {
    document.getElementById('deleteForm').action = url;
    openModal('deleteModal');
}