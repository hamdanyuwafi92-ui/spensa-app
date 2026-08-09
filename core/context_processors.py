from core.models import Brand, School, ActiveYear
from core.utilities.access import get_user_jobs
from core.utilities.constants import LEVEL_CHOICES, SUBJECT_CHOICES


def user_has_access(user, allowed_jobs):
    user_jobs = get_user_jobs(user)
    if not user_jobs:
        return False
    return any(job in allowed_jobs for job in user_jobs)


def global_data(request):
    brand = Brand.get_solo()
    school = School.get_solo()
    active_year = ActiveYear.get_active()
    user = request.user

    all_menus = [
        {
            "category": "Utama",
            "items": [
                {
                    "name": "Dashboard",
                    "url": "/core/",
                    "icon": "fa-house",
                    "allowed_jobs": [
                        "Developer",
                        "Administrator",
                        "Agent",
                        "Guru",
                        "Siswa",
                    ],
                },
                {
                    "name": "Report & Analytic",
                    "url": "/core/report/",
                    "icon": "fa-chart-pie",
                    "allowed_jobs": ["Developer", "Administrator"],
                },
                {
                    "name": "Profil",
                    "url": "/core/profile/",
                    "icon": "fa-user",
                    "allowed_jobs": [
                        "Developer",
                        "Administrator",
                        "Agent",
                        "Guru",
                        "Siswa",
                    ],
                },
                {
                    "name": "Riwayat Mengajar",
                    "url": "/core/logteaching/",
                    "icon": "fa-clock",
                    "allowed_jobs": ["Guru"],
                },
                {
                    "name": "Riwayat Pelatih",
                    "url": "/core/logagent/",
                    "icon": "fa-clock",
                    "allowed_jobs": ["Agent"],
                },
                {
                    "name": "Riwayat Nilai",
                    "url": "/core/loglearning/",
                    "icon": "fa-star",
                    "allowed_jobs": ["Siswa"],
                },
            ],
        },
        {
            "category": "Blog",
            "items": [
                {
                    "name": "Lihat Situs",
                    "url": "/",
                    "icon": "fa-arrow-up-right-from-square",
                    "allowed_jobs": [
                        "Developer",
                        "Administrator",
                        "Agent",
                        "Guru",
                        "Siswa",
                    ],
                },
                {
                    "name": "Artikel",
                    "url": "/core/article/",
                    "icon": "fa-newspaper",
                    "allowed_jobs": [
                        "Developer",
                        "Administrator",
                        "Agent",
                        "Guru",
                        "Siswa",
                    ],
                },
                {
                    "name": "Album",
                    "url": "/core/album/",
                    "icon": "fa-images",
                    "allowed_jobs": [
                        "Developer",
                        "Administrator",
                        "Agent",
                        "Guru",
                        "Siswa",
                    ],
                },
            ],
        },
        {
            "category": "Akademik",
            "items": [
                {
                    "name": "Tahun Ajaran",
                    "url": "/core/year/",
                    "icon": "fa-calendar",
                    "allowed_jobs": ["Developer", "Administrator"],
                },
                {
                    "name": "Kelas & Mapel",
                    "url": "/core/subjectroom/",
                    "icon": "fa-book",
                    "allowed_jobs": ["Developer", "Administrator"],
                },
                {
                    "name": "Ekstrakurikuler",
                    "url": "/core/club/",
                    "icon": "fa-futbol",
                    "allowed_jobs": ["Developer", "Administrator"],
                },
            ],
        },
        {
            "category": "Manajemen",
            "items": [
                {
                    "name": "Kelas Aktif",
                    "url": "/core/activeclass/",
                    "icon": "fa-users",
                    "allowed_jobs": ["Developer", "Administrator"],
                },
                {
                    "name": "Mapel Aktif",
                    "url": "/core/activesubject/",
                    "icon": "fa-chalkboard",
                    "allowed_jobs": ["Developer", "Administrator"],
                },
                {
                    "name": "Klub Aktif",
                    "url": "/core/activeclub/",
                    "icon": "fa-flag",
                    "allowed_jobs": ["Developer", "Administrator"],
                },
            ],
        },
        {
            "category": "Penilaian",
            "items": [
                {
                    "name": "Formatif",
                    "url": "/core/formatif/",
                    "icon": "fa-pen",
                    "allowed_jobs": ["Guru"],
                },
                {
                    "name": "Sumatif",
                    "url": "/core/sumatif/",
                    "icon": "fa-check",
                    "allowed_jobs": ["Guru"],
                },
                {
                    "name": "Ekstrakurikuler",
                    "url": "/core/performance/",
                    "icon": "fa-medal",
                    "allowed_jobs": ["Agent"],
                },
                {
                    "name": "Transkrip Nilai",
                    "url": "/core/transcript/",
                    "icon": "fa-file-alt",
                    "allowed_jobs": ["Guru"],
                },
            ],
        },
        {
            "category": "Konfigurasi",
            "items": [
                {
                    "name": "Brand",
                    "url": "/core/brand/",
                    "icon": "fa-copyright",
                    "allowed_jobs": ["Developer"],
                },
                {
                    "name": "Sekolah",
                    "url": "/core/school/",
                    "icon": "fa-school",
                    "allowed_jobs": ["Developer", "Administrator"],
                },
                {
                    "name": "Guru",
                    "url": "/core/teacher/",
                    "icon": "fa-chalkboard-teacher",
                    "allowed_jobs": ["Developer", "Administrator"],
                },
                {
                    "name": "Siswa",
                    "url": "/core/student/",
                    "icon": "fa-user-graduate",
                    "allowed_jobs": ["Developer", "Administrator"],
                },
                {
                    "name": "Halaman",
                    "url": "/core/page/",
                    "icon": "fa-file",
                    "allowed_jobs": ["Developer", "Administrator"],
                },
                {
                    "name": "Pengaturan",
                    "url": "/core/settings/",
                    "icon": "fa-cog",
                    "allowed_jobs": ["Developer", "Administrator"],
                },
            ],
        },
    ]

    filtered_menus = []
    for category in all_menus:
        visible_items = [
            item
            for item in category["items"]
            if user_has_access(user, item["allowed_jobs"])
        ]
        if visible_items:
            filtered_menus.append(
                {"category": category["category"], "items": visible_items}
            )

    return {
        "brand": brand,
        "school": school,
        "active_year": active_year,
        "menus": filtered_menus,
        "level_choices": LEVEL_CHOICES,
        "subject_choices": SUBJECT_CHOICES,
    }
