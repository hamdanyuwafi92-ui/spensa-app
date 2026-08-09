function showToast(title, message, iconClass, colorVar) {
    const container = document.getElementById('toastContainer');
    if (!container) return;
    const toast = document.createElement('div');
    toast.className = 'toast-item';
    toast.innerHTML = `
        <div class="toast-icon" style="color: var(${colorVar})">
            <i class="${iconClass}"></i>
        </div>
        <div class="toast-body">
            <h4>${title}</h4>
            <p>${message}</p>
        </div>
    `;
    container.appendChild(toast);
    setTimeout(() => {
        if (container.contains(toast)) toast.remove();
    }, SPENSA.toastDuration);
}