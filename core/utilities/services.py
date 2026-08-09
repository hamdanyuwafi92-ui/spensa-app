def create_user_for_person(instance):
    from django.contrib.auth import get_user_model

    User = get_user_model()
    if instance.user is not None:
        return None
    if hasattr(instance, "nip"):
        username = instance.nip
        password = "guruoke123"
        job = instance.job
    else:
        username = instance.nisn
        password = "siswaoke123"
        job = "Siswa"

    user = User.objects.create_user(username=username, password=password)
    user.is_active = True
    if job == "Developer":
        user.is_staff = True
        user.is_superuser = True
    elif job in ("Administrator", "Agent", "Guru"):
        user.is_staff = True
    user.save()
    return user
