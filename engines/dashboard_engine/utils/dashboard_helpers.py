from engines.profile_engine.models import Profile


def util_profile(profile: Profile | None) -> dict:
    if not profile:
        return {
            "display_name": False,
            "headline": False,
            "bio": False,
            "phone_number": False,
            "country": False,
            "city": False,
            "website": False,
            "github_url": False,
        }
    display_name = bool(profile.display_name)
    bool(profile.headline),
    headline = bool(profile.headline)
    bio = bool(profile.bio)
    phone_number = bool(profile.phone_number)
    country = bool(profile.country)
    city = bool(profile.city)
    website = bool(profile.website)
    github_url = bool(profile.github_url)
    linkedin_url = bool(profile.linkedin_url)
    date_of_birth = bool(profile.date_of_birth)
    is_public = bool(profile.is_public)
    created_at = bool(profile.created_at)
    updated_at = bool(profile.updated_at)   

    return {
        "display_name": display_name,
        "headline": headline,
        "bio": bio,
        "phone_number": phone_number,
        "country": country,
        "city": city,
        "website": website,
        "github_url": github_url,
        "linkedin_url": linkedin_url,
        "date_of_birth": date_of_birth,
        "is_public": is_public,
        "created_at": created_at,
        "updated_at": updated_at,
    }