document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    const toggleBtn = document.getElementById('navToggle');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            sidebar?.classList.toggle('active');
            overlay?.classList.toggle('active');
        });
        overlay?.addEventListener('click', () => {
            sidebar?.classList.remove('active');
            overlay?.classList.remove('active');
        });
    }

    const userDropdown = document.getElementById('userDropdown');
    if (userDropdown) {
        const avatarBtn = userDropdown.querySelector('.avatar-btn');
        if (avatarBtn) {
            avatarBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                userDropdown.classList.toggle('active');
                avatarBtn.setAttribute('aria-expanded', userDropdown.classList.contains('active'));
            });
        }
        document.addEventListener('click', (e) => {
            if (!userDropdown.contains(e.target)) {
                userDropdown.classList.remove('active');
                avatarBtn?.setAttribute('aria-expanded', 'false');
            }
        });
    }

    qsa('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const target = document.getElementById(btn.dataset.target);
            if (!target) return;
            qsa('.tab-btn').forEach(b => b.classList.remove('active'));
            qsa('.tab-content').forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            target.classList.add('active');
        });
    });

    const modalOverlay = document.getElementById('customModal');
    if (modalOverlay) {
        const openBtn = document.getElementById('btnModal');
        const closeBtn = document.getElementById('closeModal');
        const actionBtn = document.getElementById('modalActionBtn');
        openBtn?.addEventListener('click', () => modalOverlay.classList.add('active'));
        closeBtn?.addEventListener('click', () => modalOverlay.classList.remove('active'));
        actionBtn?.addEventListener('click', () => modalOverlay.classList.remove('active'));
        modalOverlay.addEventListener('click', (e) => {
            if (e.target === modalOverlay) modalOverlay.classList.remove('active');
        });
    }

    const lsInput = document.getElementById('liveSearchInput');
    const lsResult = document.getElementById('liveSearchResult');
    if (lsInput && lsResult) {
        const lsItems = qsa('.ls-item', lsResult);
        lsInput.addEventListener('input', (e) => {
            const val = e.target.value.toLowerCase();
            if (val.length > 0) {
                lsResult.classList.add('active');
                let found = false;
                lsItems.forEach(item => {
                    const text = item.textContent.toLowerCase();
                    if (text.includes(val)) {
                        item.style.display = 'block';
                        found = true;
                    } else {
                        item.style.display = 'none';
                    }
                });
                if (!found) lsResult.classList.remove('active');
            } else {
                lsResult.classList.remove('active');
            }
        });
        lsItems.forEach(item => {
            item.addEventListener('click', () => {
                lsInput.value = item.textContent;
                lsResult.classList.remove('active');
            });
        });
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.live-search-wrapper')) {
                lsResult.classList.remove('active');
            }
        });
    }

    const btnSave = document.getElementById('btnSave');
    const btnExport = document.getElementById('btnExport');
    const btnDelete = document.getElementById('btnDelete');
    const btnRefresh = document.getElementById('btnRefresh');
    btnSave?.addEventListener('click', () => showToast('Sukses', 'Data berhasil disimpan.', 'fa-solid fa-circle-check', '--word'));
    btnExport?.addEventListener('click', () => showToast('Ekspor', 'File Excel sedang dibuat.', 'fa-solid fa-file-excel', '--excel'));
    btnDelete?.addEventListener('click', () => showToast('Peringatan', 'Data telah dihapus permanen.', 'fa-solid fa-triangle-exclamation', '--access'));
    btnRefresh?.addEventListener('click', () => showToast('Sinkronisasi', 'Menyambung ke layanan cloud...', 'fa-solid fa-rotate', '--onenote'));
});