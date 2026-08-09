document.addEventListener('DOMContentLoaded', function () {
    const inputs = document.querySelectorAll('input[type="number"]');
    inputs.forEach(input => {
        input.addEventListener('input', function () {
            this.value = Math.round(this.value);
            if (this.value < 0) this.value = 0;
            if (this.value > 100) this.value = 100;
        });
    });
});