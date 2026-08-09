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

function editActiveClass(id, activeyear_id, classroom_id, capacity, teacher_id) {
    openModal('modalActiveClassForm', '/core/activeclass/' + id + '/update/');
    document.getElementById('modalActiveClassTitle').textContent = 'Edit Kelas Aktif';
    document.getElementById('id_activeyear').value = activeyear_id;
    document.getElementById('id_classroom').value = classroom_id;
    document.getElementById('id_capacity').value = capacity;
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

document.addEventListener('DOMContentLoaded', function () {
    var searchInput = document.getElementById('studentSearchInput');
    var searchResults = document.getElementById('studentSearchResults');
    var selectedStudent = document.getElementById('selectedStudent');
    var submitBtn = document.getElementById('submitStudentBtn');

    if (!searchInput || !searchResults) return;

    var studentData = window.allStudents || [];

    searchInput.addEventListener('input', function () {
        var val = this.value.trim().toLowerCase();
        if (val.length < 2) {
            searchResults.classList.remove('active');
            return;
        }
        var filtered = studentData.filter(function (s) {
            return s.name.toLowerCase().indexOf(val) !== -1 || s.nisn.indexOf(val) !== -1;
        });
        if (filtered.length === 0) {
            searchResults.innerHTML = '<div class="ss-item">Siswa tidak ditemukan</div>';
        } else {
            searchResults.innerHTML = filtered.map(function (s) {
                return '<div class="ss-item" data-id="' + s.id + '">' + s.nisn + ' - ' + s.name + '</div>';
            }).join('');
        }
        searchResults.classList.add('active');
    });

    searchResults.addEventListener('click', function (e) {
        var item = e.target.closest('.ss-item');
        if (item && item.dataset.id) {
            selectedStudent.value = item.dataset.id;
            searchInput.value = item.textContent;
            searchResults.classList.remove('active');
            submitBtn.disabled = false;
        }
    });

    document.addEventListener('click', function (e) {
        if (!e.target.closest('.student-search-wrapper')) {
            searchResults.classList.remove('active');
        }
    });
});