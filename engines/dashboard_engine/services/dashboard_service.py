from engines.dashboard_engine.schemas.dashboard_schema import (
    DashboardDataSchema,
    DashboardSummarySchema,
)

def get_dashboard_data() -> DashboardDataSchema:
    return DashboardDataSchema(
        display_name="Demo Builder",
        headline="Building modular systems with CodeEraX.",
        bio="I am a developer who loves to build modular systems with CodeEraX.",
        phone_number="1234567890",
        country="United States",
        city="New York",
        website="https://codeerax.dev",
        github_url="https://github.com/codeerax",
        linkedin_url="https://linkedin.com/in/codeerax",
        date_of_birth="1990-01-01",
        is_public=True,
        message="Dashboard fetched successfully (dummy data).",
    )


def get_dashboard_summary() -> DashboardSummarySchema:
    return DashboardSummarySchema(
        display_name="Demo Builder",
        headline="Building modular systems with CodeEraX.",
        bio="I am a developer who loves to build modular systems with CodeEraX.",
        phone_number="1234567890",
        country="United States",
        website="https://codeerax.dev",
        github_url="https://github.com/codeerax",
        linkedin_url="https://linkedin.com/in/codeerax",
    )





# THIS IS FOR REAL LIFE USE CASES WHERE WE NEED TO FETCH THE DATA FROM THE DATABASE

# def get_dashboard_summary() -> DashboardSummarySchema:
#     profile = Profile.objects.get(user__username="demo_builder")
#     return DashboardSummarySchema(
#         display_name=profile.display_name,
#         headline=profile.headline,
#         bio=profile.bio,
#         phone_number=profile.phone_number,
#         country=profile.country,
#         website=profile.website,
#         github_url=profile.github_url,
#         linkedin_url=profile.linkedin_url,
#         message="Dashboard summary fetched successfully (dummy data).",
#     )




# from engines.dashboard_engine.utils.dashboard_helpers import util_profile
# from engines.profile_engine.models import Profile


# def get_dashboard_data() -> DashboardDataSchema:
#     profile = Profile.objects.get(user__username="demo_builder")
#     return DashboardDataSchema(**util_profile(profile))


# def get_dashboard_summary() -> DashboardSummarySchema:
#     profile = Profile.objects.get(user__username="demo_builder")
#     return DashboardSummarySchema(**util_profile(profile))