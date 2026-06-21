## Dashboard Engine Documentation

This document explains how `engines/dashboard_engine` works end-to-end in the current codebase.

## 1) Purpose

The `dashboard_engine` is a backend module that exposes dashboard data through API endpoints.

Current state:
- It is intentionally using **dummy/static data** (no DB dependency for the live response path).
- Endpoints are **public** for now (`AllowAny`), so they can be opened directly in browser/curl.
- It follows a modular engine pattern: routes -> controllers -> services -> schemas.

## 2) Where It Is Wired In

Routing is mounted from `core/urls.py`:
- `path("dashboard", include("engines.dashboard_engine.routes"))`
- `path("dashboard/", include("engines.dashboard_engine.routes"))`

This means both URL styles are accepted:
- `/dashboard`
- `/dashboard/`
- `/dashboard/summary/`

## 3) File-by-File Architecture

### `engines/dashboard_engine/routes/dashboard_routes.py`
Defines endpoint URL patterns:
- `""` -> `DashboardView` (main dashboard payload)
- `"summary/"` -> `DashboardSummaryView` (summary payload)

### `engines/dashboard_engine/controllers/dashboard_controller.py`
Contains DRF API views:
- `DashboardView.get()`
  - Calls `get_dashboard_data()`
  - Returns JSON with HTTP 200
- `DashboardSummaryView.get()`
  - Calls `get_dashboard_summary()`
  - Returns JSON with HTTP 200

Important:
- `permission_classes = [AllowAny]`
- No authentication classes are applied here currently.

### `engines/dashboard_engine/services/dashboard_service.py`
Holds business/data assembly logic:
- `get_dashboard_data() -> DashboardDataSchema`
  - Returns detailed dummy profile/dashboard-like object
- `get_dashboard_summary() -> DashboardSummarySchema`
  - Returns compact dummy summary object

This is the correct layer to evolve when switching from dummy data to DB or external service data.

### `engines/dashboard_engine/schemas/dashboard_schema.py`
Defines dataclass contracts returned by services:
- `DashboardDataSchema`
- `DashboardSummarySchema`

Controllers return `data.__dict__`, so schema fields become JSON keys.

### `engines/dashboard_engine/utils/dashboard_helpers.py`
Contains helper utility `util_profile(profile)` for profile-field boolean mapping.

Current status:
- Not used in active endpoint flow right now.
- Can be used later when connecting real profile records to dashboard composition.

### `engines/dashboard_engine/engine_config.py`
Provides a registration function:
- `register_dashboard_engine()`

At the moment, engine is mounted directly via `core/urls.py`, so this file is optional in active routing flow.

## 4) Runtime Request Flow

For `GET /dashboard/summary/` (same idea for `/dashboard`):

1. Request enters Django URL resolver (`core/urls.py`).
2. It is delegated to `engines.dashboard_engine.routes`.
3. `dashboard_routes.py` maps it to `DashboardSummaryView`.
4. Controller calls service function `get_dashboard_summary()`.
5. Service builds `DashboardSummarySchema` dummy object.
6. Controller serializes via `__dict__` and returns JSON response.

## 5) Response Shape (Current)

### `GET /dashboard`
Returns a detailed object containing fields like:
- `display_name`
- `headline`
- `bio`
- `phone_number`
- `country`
- `city`
- `website`
- `github_url`
- `linkedin_url`
- `date_of_birth`
- `is_public`
- `message`

### `GET /dashboard/summary/`
Returns a compact object containing fields like:
- `display_name`
- `headline`
- `bio`
- `phone_number`
- `country`
- `website`
- `github_url`
- `linkedin_url`

## 6) Why This Fits The Current Stage

This implementation matches early-stage expectations:
- quick to demo
- modular enough to scale
- easy to replace dummy service logic with real aggregation later
- no auth friction while endpoints are still under active prototyping

## 7) Next Upgrade Path (When You Move to Real Data)

When production wiring starts, keep controllers/routes same and only change internals:

1. Keep endpoint contracts stable (`schemas` first).
2. Update service functions to fetch from:
   - `auth_engine` user
   - `profile_engine` profile
   - other engine outputs as needed
3. Re-introduce authentication in controllers:
   - `JWTAuthentication`
   - `IsAuthenticatedCustom`
4. Keep `utils/` for profile completeness and summary calculations.
5. Add tests for both endpoints and schema integrity.

## 8) Quick Smoke Test

Run server:

```bash
python manage.py runserver
```

Test:

```bash
curl http://127.0.0.1:8000/dashboard
curl http://127.0.0.1:8000/dashboard/summary/
```

Expected:
- HTTP 200 responses with dummy JSON payloads.

