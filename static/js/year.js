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

function editYear(id, name) {
    openModal('modalYearForm', '/core/year/year/' + id + '/update/');
    document.getElementById('modalYearTitle').textContent = 'Edit Tahun';
    document.querySelector('#yearForm [name="name"]').value = name;
}

function editSemester(id, name) {
    openModal('modalSemesterForm', '/core/year/semester/' + id + '/update/');
    document.getElementById('modalSemesterTitle').textContent = 'Edit Semester';
    document.querySelector('#semesterForm [name="name"]').value = name;
}

function editActiveYear(id, yearId, semesterId, isActive) {
    openModal('modalActiveForm', '/core/year/active/' + id + '/update/');
    document.getElementById('modalActiveTitle').textContent = 'Edit Tahun Aktif';
    document.getElementById('activeYearSelect').value = yearId;
    document.getElementById('activeSemesterSelect').value = semesterId;
    document.getElementById('activeIsActive').checked = (isActive === 'true');
}

function confirmDelete(url) {
    if (url.indexOf('/year/year/') !== -1) {
        document.getElementById('deleteYearForm').action = url;
        openModal('deleteYearModal');
    } else if (url.indexOf('/year/semester/') !== -1) {
        document.getElementById('deleteSemesterForm').action = url;
        openModal('deleteSemesterModal');
    } else if (url.indexOf('/year/active/') !== -1) {
        document.getElementById('deleteActiveForm').action = url;
        openModal('deleteActiveModal');
    }
}