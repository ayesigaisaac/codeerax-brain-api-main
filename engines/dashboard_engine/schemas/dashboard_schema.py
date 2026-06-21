from dataclasses import dataclass

@dataclass
class DashboardDataSchema:
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
    message: str | None = None


@dataclass
class DashboardSummarySchema:
    display_name: str | None = None
    headline: str | None = None
    bio: str | None = None
    phone_number: str | None = None
    country: str | None = None
    website: str | None = None
    github_url: str | None = None
    linkedin_url: str | None = None

