LEVEL_CHOICES = tuple((str(i), str(i)) for i in range(1, 13))

SUBJECT_CHOICES = (
    ("PKN", "Pendidikan Kewarganegaraan"),
    ("BIND", "Bahasa Indonesia"),
    ("BIG", "Bahasa Inggris"),
    ("MAT", "Matematika"),
    ("IPA", "Ilmu Pengetahuan Alam"),
    ("IPS", "Ilmu Pengetahuan Sosial"),
    ("SBK", "Seni Budaya"),
    ("PJOK", "Pendidikan Jasmani Olahraga dan Kesehatan"),
    ("PRAKARYA", "Prakarya"),
    ("TIK", "Teknologi Informasi dan Komunikasi"),
    ("MULOK", "Muatan Lokal"),
    ("PAI", "Pendidikan Agama Islam"),
    ("PAK", "Pendidikan Agama Kristen"),
    ("PAKH", "Pendidikan Agama Katolik"),
    ("PAH", "Pendidikan Agama Hindu"),
    ("PAB", "Pendidikan Agama Buddha"),
    ("PAKONG", "Pendidikan Agama Khonghucu"),
    ("QURDIS", "Al-Qur'an Hadis"),
    ("AQIDAH", "Akidah Akhlak"),
    ("FIQIH", "Fikih"),
    ("SKI", "Sejarah Kebudayaan Islam"),
    ("B_ARAB", "Bahasa Arab"),
    ("FIS", "Fisika"),
    ("KIM", "Kimia"),
    ("BIO", "Biologi"),
    ("SEJ", "Sejarah"),
    ("GEO", "Geografi"),
    ("EKO", "Ekonomi"),
    ("SOS", "Sosiologi"),
    ("MTK_PEM", "Matematika Peminatan"),
    ("FIS_PEM", "Fisika Peminatan"),
    ("KIM_PEM", "Kimia Peminatan"),
    ("BIO_PEM", "Biologi Peminatan"),
    ("SEJ_PEM", "Sejarah Peminatan"),
    ("GEO_PEM", "Geografi Peminatan"),
    ("EKO_PEM", "Ekonomi Peminatan"),
    ("SOS_PEM", "Sosiologi Peminatan"),
    ("TAFSIR", "Ilmu Tafsir"),
    ("HADIS", "Ilmu Hadis"),
    ("USULFIQ", "Ushul Fikih"),
    ("B_IND_MUL", "Bahasa dan Sastra Indonesia"),
    ("B_ING_MUL", "Bahasa dan Sastra Inggris"),
    ("B_ASING", "Bahasa Asing Lainnya"),
    ("SIMDIG", "Simulasi Digital"),
    ("DASDES", "Dasar Desain Grafis"),
    ("PEMROG", "Pemrograman Dasar"),
    ("JARINGAN", "Dasar Jaringan Komputer"),
    ("KWU", "Kewirausahaan"),
)

TEACHER_JOB_CHOICES = (
    ("Developer", "Developer"),
    ("Administrator", "Administrator"),
    ("Agent", "Agent"),
    ("Guru", "Guru"),
)

STUDENT_JOB_CHOICES = (("Siswa", "Siswa"),)

GENDER_CHOICES = (
    ("Laki-laki", "Laki-laki"),
    ("Perempuan", "Perempuan"),
)

STUDENT_STATUS_CHOICES = (
    ("Aktif", "Aktif"),
    ("Lulus", "Lulus"),
    ("Keluar", "Keluar"),
)

TAG_CHOICES = (
    ("Berita", "Berita"),
    ("Pengumuman", "Pengumuman"),
    ("Kegiatan", "Kegiatan"),
    ("Prestasi", "Prestasi"),
    ("Info", "Info"),
)
