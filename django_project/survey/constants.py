from django.utils.translation import gettext_lazy as _
from django.conf import settings

GENDER_CHOICES = (
    ("Male", _("Male")),
    ("Female", _("Female"))
    )



CUSTOM_MAP_SETTINGS = {
    "GooglePointFieldWidget": (
        ("zoom", 15),
        ("mapCenterLocation", [-15.7177013, 28.6300491]),
    ),
}


BASE_TEMP_DIR = f"{settings.MEDIA_ROOT}/temp/"

