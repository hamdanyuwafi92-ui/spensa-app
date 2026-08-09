from .activeclass import urlpatterns as activeclass_urls
from .activeclub import urlpatterns as activeclub_urls
from .activesubject import urlpatterns as activesubject_urls
from .album import urlpatterns as album_urls
from .blog import urlpatterns as blog_urls
from .brand import urlpatterns as brand_urls
from .club import urlpatterns as club_urls
from .index import urlpatterns as index_urls
from .page import urlpatterns as page_urls
from .profile import urlpatterns as profile_urls
from .school import urlpatterns as school_urls
from .student import urlpatterns as student_urls
from .subjectroom import urlpatterns as subjectroom_urls
from .sync import urlpatterns as sync_urls
from .teacher import urlpatterns as teacher_urls
from .year import urlpatterns as year_urls
from .report import urlpatterns as report_urls
from .logteaching import urlpatterns as logteaching_urls
from .loglearning import urlpatterns as loglearning_urls
from .logagent import urlpatterns as logagent_urls
from .formatif import urlpatterns as formatif_urls
from .sumatif import urlpatterns as sumatif_urls
from .performance import urlpatterns as performance_urls
from .transcript import urlpatterns as transcript_urls
from .backup import urlpatterns as backup_urls

urlpatterns = (
    index_urls
    + blog_urls
    + album_urls
    + page_urls
    + year_urls
    + subjectroom_urls
    + club_urls
    + activeclass_urls
    + activesubject_urls
    + activeclub_urls
    + teacher_urls
    + student_urls
    + profile_urls
    + school_urls
    + brand_urls
    + sync_urls
    + report_urls
    + logteaching_urls
    + loglearning_urls
    + logagent_urls
    + formatif_urls
    + sumatif_urls
    + performance_urls
    + transcript_urls
    + backup_urls
)
