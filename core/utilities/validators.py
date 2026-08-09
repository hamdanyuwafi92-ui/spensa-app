from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validate_logo(value):
    valid_extensions = [".png", ".jpg", ".jpeg"]
    ext = value.name.lower().rsplit(".", 1)[-1]
    if f".{ext}" not in valid_extensions:
        raise ValidationError("Format logo harus PNG, JPG, atau JPEG.")
    if value.size > 2 * 1024 * 1024:
        raise ValidationError("Ukuran logo maksimal 2 MB.")


validate_npsn = RegexValidator(
    regex=r"^\d{8}$",
    message="NPSN harus terdiri dari 8 digit angka.",
)

validate_nip = RegexValidator(
    regex=r"^\d{18}$",
    message="NIP harus terdiri dari 18 digit angka.",
)

validate_nuptk = RegexValidator(
    regex=r"^\d{16}$",
    message="NUPTK harus terdiri dari 16 digit angka.",
)

validate_nisn = RegexValidator(
    regex=r"^\d{10}$",
    message="NISN harus terdiri dari 10 digit angka.",
)

validate_nis = RegexValidator(
    regex=r"^\d{10}$",
    message="NIS harus terdiri dari 10 digit angka.",
)

validate_kode_pos = RegexValidator(
    regex=r"^\d{5}$",
    message="Kode pos harus terdiri dari 5 digit angka.",
)

validate_phone = RegexValidator(
    regex=r"^(\+62|62|0)8[1-9][0-9]{6,10}$",
    message="Nomor telepon tidak valid. Gunakan format Indonesia (08xx...).",
)

validate_fax = RegexValidator(
    regex=r"^[\d\-]{5,15}$",
    message="Nomor fax tidak valid. Gunakan hanya angka dan strip (misal 021-123456).",
)


def validate_teacher_job(teacher):
    allowed_jobs = ["Guru", "Developer", "Administrator", "Agent"]
    if teacher and teacher.job not in allowed_jobs:
        raise ValidationError(
            f"Guru dengan job '{teacher.job}' tidak diizinkan. "
            f"Hanya {', '.join(allowed_jobs)} yang diperbolehkan."
        )
