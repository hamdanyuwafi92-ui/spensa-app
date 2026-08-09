document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form[action*="cari"]');
    if (form) {
        const input = form.querySelector('input[name="q"]');
        if (input) input.focus();
    }
});