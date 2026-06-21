## Profile Engine Documentation 

## Overview

The Profile Engine manages user profile data in the CodeEraX Brain API.

It follows the same architectural pattern used in the Auth Engine:

`routes -> views -> serializers -> schemas -> services -> models`

This engine is linked to the authenticated user through a `OneToOneField`
from `Profile` to `auth_engine.User`.

## Structure

- `models.py`: profile data model and database structure
- `routes.py`: endpoint registration for the profile engine
- `views.py`: DRF API views that receive requests and return responses
- `serializers.py`: request validation layer
- `schemas.py`: lightweight data transfer objects for service calls
- `services.py`: profile business logic
- `migrations/`: database migration files
- `engine_config.py`: engine registration helper for gateway-style routing

## Endpoints

Base path:

`/profile/`

Available endpoints:

- `POST /profile/create/`
  Creates a profile for the authenticated user.

- `GET /profile/me/`
  Returns the authenticated user's profile. If no profile exists yet, a
  starter profile is created automatically.

- `POST /profile/update/`
  Updates the authenticated user's profile.

- `GET /profile/public/<uuid:user_id>/`
  Returns the public profile for a given user ID.

## Authentication

Protected endpoints use the same custom JWT authentication class from the
Auth Engine:

- `CreateProfileView`
- `MyProfileView`
- `UpdateProfileView`

The public profile endpoint uses `AllowAny`.

## Current Behavior

- Each user can have only one profile.
- Public profile access is controlled by the `is_public` field.
- Starter defaults are applied for early integration and mock-friendly usage.
- Update requests only change fields that are explicitly sent.

## Main Files

- `models.py`
- `routes.py`
- `views.py`
- `serializers.py`
- `schemas.py`
- `services.py`

## Notes

- The engine is designed to integrate directly with Auth through `user_id`.
- The current implementation is suitable for the integration phase and can be
  extended with more validation, profile fields, and richer business rules.
