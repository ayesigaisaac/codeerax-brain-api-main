from dataclasses import dataclass


UNSET = object()


@dataclass
class CreateProfileSchema:
    display_name: object = UNSET
    headline: object = UNSET
    bio: object = UNSET
    phone_number: object = UNSET
    country: object = UNSET
    city: object = UNSET
    website: object = UNSET
    github_url: object = UNSET
    linkedin_url: object = UNSET
    date_of_birth: object = UNSET
    is_public: object = UNSET


@dataclass
class UpdateProfileSchema:
    display_name: object = UNSET
    headline: object = UNSET
    bio: object = UNSET
    phone_number: object = UNSET
    country: object = UNSET
    city: object = UNSET
    website: object = UNSET
    github_url: object = UNSET
    linkedin_url: object = UNSET
    date_of_birth: object = UNSET
    is_public: object = UNSET


@dataclass
class PublicProfileSchema:
    user_id: str


@dataclass
class ProfileOutputSchema:
    profile_id: str
    user_id: str
    email: str | None = None
    username: str | None = None
    display_name: str | None = None
    headline: str | None = None
    bio: str | None = None
    phone_number: str | None = None
    country: str | None = None
    city: str | None = None
    website: str | None = None
    github_url: str | None = None
    linkedin_url: str | None = None
    date_of_birth: str | None = None
    is_public: bool | None = None
    created_at: str | None = None
    updated_at: str | None = None
    message: str | None = None
