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

function editClassroom(id, mainclassroom, name) {
    openModal('modalClassroomForm', '/core/subjectroom/classroom/' + id + '/update/');
    document.getElementById('modalClassroomTitle').textContent = 'Edit Kelas';
    document.getElementById('classroomMain').value = mainclassroom;
    document.querySelector('#classroomForm [name="name"]').value = name;
}

function editSubject(id, code, name) {
    openModal('modalSubjectForm', '/core/subjectroom/subject/' + id + '/update/');
    document.getElementById('modalSubjectTitle').textContent = 'Edit Mapel';
    document.getElementById('subjectCode').value = code;
    document.getElementById('subjectNameSelect').value = code;
}

function confirmDeleteClassroom(url) {
    document.getElementById('deleteClassroomForm').action = url;
    openModal('deleteClassroomModal');
}

function confirmDeleteSubject(url) {
    document.getElementById('deleteSubjectForm').action = url;
    openModal('deleteSubjectModal');
}