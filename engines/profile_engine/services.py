from rest_framework.exceptions import ValidationError

from .models import Profile
from .schemas import (
    CreateProfileSchema,
    ProfileOutputSchema,
    PublicProfileSchema,
    UNSET,
    UpdateProfileSchema,
)


def _default_display_name(user) -> str:
    if user.username:
        return user.username
    return user.email.split("@")[0]


def _build_profile_defaults(user) -> dict:
    return {
        "display_name": _default_display_name(user),
        "headline": "CodeEraX builder",
        "bio": "This is a starter profile pending full platform customization.",
        "is_public": True,
    }


def _serialize_profile(profile: Profile, message: str | None = None, include_private: bool = True) -> ProfileOutputSchema:
    user = profile.user
    data = {
        "profile_id": str(profile.id),
        "user_id": str(user.id),
        "username": user.username,
        "display_name": profile.display_name or _default_display_name(user),
        "headline": profile.headline,
        "bio": profile.bio,
        "country": profile.country,
        "city": profile.city,
        "website": profile.website,
        "github_url": profile.github_url,
        "linkedin_url": profile.linkedin_url,
        "date_of_birth": profile.date_of_birth.isoformat() if profile.date_of_birth else None,
        "is_public": profile.is_public,
        "created_at": profile.created_at.isoformat() if profile.created_at else None,
        "updated_at": profile.updated_at.isoformat() if profile.updated_at else None,
        "message": message,
    }

    if include_private:
        data["email"] = user.email
        data["phone_number"] = profile.phone_number

    return data


def _assign_profile_fields(profile: Profile, data: CreateProfileSchema | UpdateProfileSchema):
    field_names = (
        "display_name",
        "headline",
        "bio",
        "phone_number",
        "country",
        "city",
        "website",
        "github_url",
        "linkedin_url",
        "date_of_birth",
    )

    for field_name in field_names:
        value = getattr(data, field_name)
        if value is not UNSET:
            setattr(profile, field_name, value)

    if data.is_public is not UNSET:
        profile.is_public = data.is_public


def create_profile(user, data: CreateProfileSchema) -> ProfileOutputSchema:
    if Profile.objects.filter(user=user).exists():
        raise ValidationError({"profile": "Profile already exists."})

    profile = Profile(user=user, **_build_profile_defaults(user))
    _assign_profile_fields(profile, data)

    if not profile.display_name:
        profile.display_name = _default_display_name(user)

    if not profile.bio:
        profile.bio = "This is a starter profile pending full platform customization."

    profile.save()

    return _serialize_profile(profile, message="Profile created successfully.")


def get_my_profile(user) -> ProfileOutputSchema:
    profile, _ = Profile.objects.get_or_create(user=user, defaults=_build_profile_defaults(user))
    return _serialize_profile(profile, message="Profile fetched successfully.")


def update_profile(user, data: UpdateProfileSchema) -> ProfileOutputSchema:
    profile, _ = Profile.objects.get_or_create(user=user, defaults=_build_profile_defaults(user))
    _assign_profile_fields(profile, data)

    if not profile.display_name:
        profile.display_name = _default_display_name(user)

    if not profile.bio:
        profile.bio = "This is a starter profile pending full platform customization."

    profile.save()

    return _serialize_profile(profile, message="Profile updated successfully.")


def get_public_profile(data: PublicProfileSchema) -> ProfileOutputSchema:
    try:
        profile = Profile.objects.select_related("user").get(user_id=data.user_id)
    except Profile.DoesNotExist:
        raise ValidationError({"profile": "Profile not found."})

    if not profile.is_public:
        raise ValidationError({"profile": "Profile is private."})

    return _serialize_profile(
        profile,
        message="Public profile fetched successfully.",
        include_private=False,
    )
