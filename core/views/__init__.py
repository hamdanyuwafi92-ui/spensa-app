from .activeclass import (
    ActiveClassCreateView,
    ActiveClassDeleteView,
    ActiveClassListView,
    ActiveClassManageView,
    ActiveClassUpdateView,
    StudentDeleteView,
)
from .activeclub import (
    ActiveClubCreateView,
    ActiveClubDeleteView,
    ActiveClubListView,
    ActiveClubManageView,
    ActiveClubUpdateView,
    ClubStudentDeleteView,
)
from .activesubject import (
    ActiveSubjectCreateView,
    ActiveSubjectDeleteView,
    ActiveSubjectListView,
    ActiveSubjectUpdateView,
)
from .album import (
    AlbumCreateView,
    AlbumDeleteView,
    AlbumListView,
    AlbumManageView,
    AlbumUpdateView,
    PhotoDeleteView,
)
from .blog import (
    ArticleCreateView,
    ArticleDeleteView,
    ArticleListView,
    ArticleUpdateView,
)
from .brand import BrandDetailView, BrandUpdateView
from .club import (
    ClubCreateView,
    ClubDeleteView,
    ClubManageView,
    ClubUpdateView,
)
from .index import IndexView
from .page import (
    PageCreateView,
    PageDeleteView,
    PageListView,
    PageUpdateView,
)
from .profile import ProfileDetailView, ProfileUpdateView
from .school import SchoolDetailView, SchoolUpdateView
from .student import (
    StudentCreateView,
    StudentDeleteView,
    StudentDetailView,
    StudentListView,
    StudentResetPasswordView,
    StudentUpdateView,
)
from .subjectroom import (
    ClassroomCreateView,
    ClassroomDeleteView,
    ClassroomUpdateView,
    SubjectCreateView,
    SubjectDeleteView,
    SubjectRoomManageView,
    SubjectUpdateView,
)
from .sync import SyncView
from .teacher import (
    TeacherCreateView,
    TeacherDeleteView,
    TeacherDetailView,
    TeacherListView,
    TeacherResetPasswordView,
    TeacherUpdateView,
)
from .year import (
    ActiveYearCreateView,
    ActiveYearDeleteView,
    ActiveYearUpdateView,
    SemesterCreateView,
    SemesterDeleteView,
    SemesterUpdateView,
    YearCreateView,
    YearDeleteView,
    YearManageView,
    YearUpdateView,
)
from .report import ReportView
from .logteaching import LogTeachingView
from .loglearning import LogLearningListView, LogLearningDetailView
from .logagent import LogAgentView
from .formatif import FormatifView
from .sumatif import SumatifView
from .performance import PerformanceView
from .transcript import (
    TranscriptView,
    TranscriptDownloadView,
    TranscriptDownloadAllView,
)
from .backup import BackupView

__all__ = [
    "ArticleCreateView",
    "BackupView",
    "TranscriptView",
    "TranscriptDownloadView",
    "TranscriptDownloadAllView",
    "PerformanceView",
    "SumatifView",
    "FormatifView",
    "LogAgentView",
    "LogLearningListView",
    "LogLearningDetailView",
    "ArticleDeleteView",
    "ArticleListView",
    "ArticleUpdateView",
    "AlbumCreateView",
    "AlbumDeleteView",
    "AlbumListView",
    "AlbumManageView",
    "AlbumUpdateView",
    "PhotoDeleteView",
    "PageCreateView",
    "PageDeleteView",
    "PageListView",
    "PageUpdateView",
    "YearManageView",
    "YearCreateView",
    "YearUpdateView",
    "YearDeleteView",
    "SemesterCreateView",
    "SemesterUpdateView",
    "SemesterDeleteView",
    "ActiveYearCreateView",
    "ActiveYearUpdateView",
    "ActiveYearDeleteView",
    "SubjectRoomManageView",
    "ClassroomCreateView",
    "ClassroomUpdateView",
    "ClassroomDeleteView",
    "SubjectCreateView",
    "SubjectUpdateView",
    "SubjectDeleteView",
    "ClubManageView",
    "ClubCreateView",
    "ClubUpdateView",
    "ClubDeleteView",
    "ActiveClassListView",
    "ActiveClassCreateView",
    "ActiveClassUpdateView",
    "ActiveClassDeleteView",
    "ActiveClassManageView",
    "StudentDeleteView",
    "ActiveSubjectListView",
    "ActiveSubjectCreateView",
    "ActiveSubjectUpdateView",
    "ActiveSubjectDeleteView",
    "ActiveClubListView",
    "ActiveClubCreateView",
    "ActiveClubUpdateView",
    "ActiveClubDeleteView",
    "ActiveClubManageView",
    "ClubStudentDeleteView",
    "TeacherListView",
    "TeacherCreateView",
    "TeacherUpdateView",
    "TeacherDeleteView",
    "TeacherDetailView",
    "TeacherResetPasswordView",
    "StudentListView",
    "StudentCreateView",
    "StudentUpdateView",
    "StudentDeleteView",
    "StudentDetailView",
    "StudentResetPasswordView",
    "ProfileDetailView",
    "ProfileUpdateView",
    "SchoolDetailView",
    "SchoolUpdateView",
    "BrandDetailView",
    "BrandUpdateView",
    "SyncView",
    "IndexView",
    "ReportView",
    "LogTeachingView",
]
