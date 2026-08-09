from core.models import Brand, Category, Page, School
from blog.models import Ads


def blog_global_data(request):
    brand = Brand.get_solo()
    school = School.get_solo()
    categories = Category.objects.all()
    pages = Page.objects.all()

    main_menus = [
        {
            "name": "Beranda",
            "url": "/",
            "active_patterns": ["index"],
        },
        {
            "name": "Profil",
            "url": "#",
            "active_patterns": ["school_detail", "teacher_list", "student_list"],
            "children": [
                {
                    "name": "Sekolah",
                    "url": "/sekolah/",
                    "active_patterns": ["school_detail"],
                },
                {
                    "name": "Tenaga Pendidik",
                    "url": "/guru/",
                    "active_patterns": ["teacher_list"],
                },
                {
                    "name": "Peserta Didik",
                    "url": "/siswa/",
                    "active_patterns": ["student_list"],
                },
            ],
        },
        {
            "name": "Artikel",
            "url": "/artikel/",
            "active_patterns": ["artikel", "single", "kategori"],
        },
        {
            "name": "Galeri",
            "url": "/galeri/",
            "active_patterns": ["galeri", "album"],
        },
        {
            "name": "Kontak",
            "url": "/kontak/",
            "active_patterns": ["kontak"],
        },
    ]

    footer_categories = [
        {"name": cat.name, "url": f"/kategori/?cat={cat.id}"} for cat in categories
    ]

    footer_quick_links = [
        {"name": "Beranda", "url": "/"},
        {"name": "Sekolah", "url": "/sekolah/"},
        {"name": "Guru", "url": "/guru/"},
        {"name": "Siswa", "url": "/siswa/"},
        {"name": "Artikel", "url": "/artikel/"},
        {"name": "Galeri", "url": "/galeri/"},
        {"name": "Kontak", "url": "/kontak/"},
    ]

    ads_leaderboard = Ads.objects.filter(type="leaderboard").first()
    ads_sidebar = Ads.objects.filter(type="skyscraper").first()

    return {
        "brand": brand,
        "school": school,
        "main_menus": main_menus,
        "pages": pages,
        "footer_categories": footer_categories,
        "footer_quick_links": footer_quick_links,
        "ads_leaderboard": ads_leaderboard,
        "ads_sidebar": ads_sidebar,
    }
