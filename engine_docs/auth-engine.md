## Auth Engine Documentation

Auth Engine – Complete Backend Documentation System Overview & Architecture

The backend system is a modular, scalable Django application designed to handle user authentication, account management, and security. It supports:

User registration, login, and logout

Email verification

Password reset and update

JWT-based authentication

Core Workflows

BASE URL: http://127.0.0.1:8000/auth/

POST /auth/register

Objective: Create a new user account with email verification.

Flow:

Client submits registration data
Data is validated
User is created (inactive)
Verification email is sent
Example Request

{ "email": "test@gmail.com", "password": "123456", "username": "kingsley" }

Example Response

{ "message": "User registered successfully. Please verify your email." }

Objective: Create a new user account with email verification.

Flow:

Client submits registration data

Data is validated by serializer

Structured via schema

Service performs:

Duplicate email check

Password hashing

User creation (inactive state)

Verification token generation

Verification email is sent

Response returned to client

Result:

User is created but not yet active POST/auth/register

Email Verification

Objective: Activate user account after email confirmation.

Flow:

Client sends verification token

Service:

Locates associated user

Validates token

Checks expiration

If valid:

Account is activated

Token is cleared

Result:

User gains access to login functionality GET/auth/verify-email

User Login

Objective: Authenticate user and issue access token.

Flow:

Client submits credentials

Serializer validates input

Service:

Retrieves user

Verifies password

Confirms account is active

JWT token is generated

Token returned to client

Result:

Client receives token for authenticated requests POST/auth/login

Protected Resource Access

Objective: Restrict access to authenticated users only.

Flow:

Client includes JWT token in request header

Authentication utility validates token

User identity is resolved

Access is granted or denied

Result:

Only authorized users access protected endpoints

Password Reset

Objective: Allow users to securely reset forgotten passwords.

Flow:

Client requests password reset

System generates reset token

Email with reset link is sent

Client submits new password with token

Service validates token and updates password

Result:

Password is securely updated POST/auth/reset-password

Logout

Objective: Invalidate active authentication token.

Flow:

Client submits logout request

Token is added to blacklist

Future use of token is rejected

Result:

Token can no longer be used POST/auth/logout

Authentication Mechanism JWT-Based Authentication

The system uses JSON Web Tokens (JWT) for stateless authentication.

Key Characteristics:

No server-side session storage

Token contains user identity

Token is verified on each request

Token Usage

Client must include token in request headers:

Authorization: Bearer

Security Considerations Password Security

Passwords are hashed before storage

Plaintext passwords are never stored

Email Verification

Prevents unauthorized or fake registrations

Token Expiry

Limits the validity of verification and reset tokens

Access Control

Protected endpoints require valid authentication

Token Blacklisting

Ensures tokens cannot be reused after logout

Request Lifecycle Summary

Every request follows this sequence:

Client Request ↓ View (entry point) ↓ Serializer (validation) ↓ Schema (structuring) ↓ Service (business logic) ↓ Model (database interaction) ↓ Response

The architecture is layered and organized as:

Client (Frontend) ↓ API Gateway (apigateway) ↓ Auth Engine (views → serializers → schemas → services → models → database) ↓ Database (PostgreSQL)

Components and Responsibilities:

Client / Frontend: Sends HTTP requests

API Gateway: Centralized routing, applies middleware (logging, authentication, rate-limiting)

Engine (auth_engine): Handles all authentication logic

Database (PostgreSQL): Stores user credentials, tokens, and metadata

Folder Structure backend/ ├── core/ │ ├── settings.py # Django settings, middleware, logging, database config │ ├── urls.py # Loads API gateway routes ├── apigateway/ │ ├── urls.py # Collects engine routers │ ├── middleware.py # Logging, auth, rate-limiting │ └── permissions.py # Centralized permission classes ├── engines/ │ └── auth_engine/ │ ├── models.py │ ├── serializers.py │ ├── schemas.py │ ├── services.py │ ├── views.py │ ├── routes.py │ └── utils/ │ ├── auth.py # JWT, password hashing │ ├── authentication.py # Custom DRF authentication │ ├── email.py # Send verification/reset emails │ └── logout.py # Token blacklisting └── utils/ # Shared helpers (logging, formatting, email)

Models

The User model represents users in the database:

Fields: id (UUID), email, username, password (hashed), is_active, email_verification_token, email_verification_expiry

Handles email verification token generation

Interacts with PostgreSQL via Django ORM

Schemas

Schemas define structured input data for services:

Example: RegisterSchema, LoginSchema, ResetPasswordSchema

Enforces type safety and structured communication between views and services

Reduces boilerplate validation in views

@dataclass class RegisterSchema: email: str password: str username: Optional[str] = None Serializers

Connect HTTP requests to schemas

Convert incoming JSON to Python objects

Handle validation and field-specific constraints

Example: RegisterSerializer calls RegisterSchema and passes validated data to service

Services

Contain all business logic: registration, login, logout, email verification, password management

Services do not handle HTTP requests; they operate on validated schema data

Examples:

Registration

Check if email exists

Hash password

Create inactive user

Generate verification token

Send verification email

Login

Verify email and password

Check account activation

Generate JWT

Update last login timestamp

Logout

Blacklists JWT tokens

Password Reset

Generate token, send email, verify token, update password

Email Verification

Verify token and expiry, activate user

Views

Handle incoming HTTP requests

Call serializers → schemas → services

Return JSON responses

Example:

class RegisterView(APIView): permission_classes = [AllowAny]

def post(self, request):
    schema = RegisterSchema(**request.data)
    data = register_user(schema)
    return Response(data, status=status.HTTP_201_CREATED)
Other views include LoginView, LogoutView, VerifyEmailView, ForgotPasswordView, ResetPasswordView.

Routes & API Gateway

Each engine defines routes.py

engine_config.py registers engine routes with API Gateway

API Gateway applies global middleware:

Logging

Authentication

Rate-limiting

Frontend sends all requests through API Gateway

Settings

Database: PostgreSQL connection configured in settings.py

Logging: Centralized for all engines

Email: SMTP backend configured for sending verification and reset emails

Installed Apps & Middleware: All engines registered

Example database config:

DATABASES = { "default": { "ENGINE": "django.db.backends.postgresql", "NAME": "brain_db", "USER": "jonah", "PASSWORD": "joel", "HOST": "localhost", "PORT": "5432", } }

Flow of a Request Frontend sends HTTP request ↓ API Gateway routes request → middleware applies logging & auth checks ↓ Engine View receives request ↓ Serializer validates request ↓ Schema structures data ↓ Service executes business logic ↓ Model interacts with PostgreSQL ↓ Service returns result ↓ View returns JSON response to frontend

Example: Registration → Schema → Service → Model → Send verification email → Response

Security & Authentication

JWT tokens for stateless authentication

Password hashing using secure algorithms

Email verification required for account activation

Token blacklisting on logout

Middleware ensures that only authenticated users can access protected endpoints

Summary

The backend system is modular, secure, and maintainable, designed to provide a reliable authentication flow:

Engines handle domain-specific logic

Views process requests and responses

Serializers & Schemas ensure structured data

Services implement business rules

Models persist data in PostgreSQL

API Gateway provides a single entry point with middleware
