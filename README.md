# Data Leak Checker

Sistema de Verificación de Filtraciones de Datos Orientado a Usuarios Chilenos

## Table of Contents

- [Getting Started](#getting-started)
- [Uploading Data](#uploading-data)
- [Environment Variables](#environment-variables)

## Getting Started

1. Clone repository
2. Set environment variables
   - Create `.env` file (use `template.env` as base)
   - Configure according your needs
3. Run with `docker compose up`
4. Populate datbase with breaches information

## Uploading Data

## Environment Variables

### Backend Related

`IN_PROD`: Indicates if environment is production. True for production  
`CORS_ORIGINS`: Allowed origins that can make cross-origin requests to the backend.  
`ROOT_ROUTE`: Path prefix for backend endpoints. Used in `root_path` setting for FastAPI.  
`HMAC_KEY`: Private key used to calculate searched identifiers HMAC value.  
`FRONTEND_URL`: Frotend's url. Used to redirection after OpenId Connect authentication  
`POPULATE_DUMMY_DATA`: Whether to populate Database with dummy data, only for demo purposes.

#### Twilio

`TWILIO_AUTH_TOKEN`: Twilio's auth token  
`TWILIO_ACCOUNT_SID`: Twilio's account SID  
`TWILIO_SENDER_NUMBER`: Twilio's phone number from message will be sent  
`DEV_RECEIVER_NUMBER`: Number that receives all sms (For development purposes)

#### SMTP / Email Sender

`SMTP_USERNAME`: Username of the SMTP server  
`SMTP_PASSWORD`: Password of that username  
`SMTP_SERVER`: Address of the SMTP server  
`SMTP_PORT`: SMTP port number (usually 25 or 587)  
`SMTP_FROM_NAME`: Custom name for the email sender

#### JWT

`JWT_SECRET`: Secret for signing JWT  
`JWT_ALGORITHM`: Algorithm used ("HS256" is used by default)

#### OpenId Connect

`CLIENT_ID`: Client ID for OpenId Connect  
`CLIENT_SECRET`: Secret for OpenId Connect communication

#### Enabled Verification Keys

`ENABLED_SEARCH_KEYS`: Specifies which identifiers / keys are searchable (default='email,phone,rut')  
`ENABLED_VERIFICATION_SEARCH_KEYS`: Specifies which identifiers/keys are enabled for authentication (default="email,phone,rut")  
`MUST_VERIFY_SEARCH_KEYS`: Specifies which identifiers/keys REQUIERE verification to search for (format="email,phon,rut", default="")

#### Cloudflare

`CLOUDFLARE_SECRET_KEY`: Secret key to verify Cloudflare Turnstile tokens  
`CLOUDFLARE_ENABLED`: Indicates whether Cloudflare Turnstile is enable

#### Verification Code

`CODE_LENGTH`: Number that specifies the length of verification codes
`CODE_EXPIRE_MINUTES`: Indicates the amount of minutes the verification code is valid for  
`MAX_CODE_TRIES`: Maximum number of tries before invalidating a verification code
`MAX_CODES_CREATED`: Maximum number of verification codes created by the same IP address.  
`CODE_MINUTES_RANGE_LIMIT`: Time interval in minutes that the same IP address can generate the maximum amount of verification codes

---

### Database Related

`POSTGRES_USER`: PostgreSQL user  
`PGUSER`: PostgreSQL user  
`POSTGRES_PASSWORD`: User's password  
`POSTGRES_DB`: Database name  
`POSTGRES_TEST_DB`: Test database name  
`POSTGRES_SERVER`: PostgreSQL server's address

---

### Frontend Related

`NEXT_PUBLIC_BACKEND_URL`: Backend's API url  
`NEXT_PUBLIC_PROD`: Indicates whether the environment is on production. true for production.  
`NEXT_PUBLIC_ENABLED_SEARCH_KEYS`: Indicates which identifiers are available for search (default="email,phone,rut")  
`NEXT_PUBLIC_ENABLED_VERIFICATION_SEARCH_KEYS`: Indicates which identifiers are available for authentication (default="email,phone,rut")  
`NEXT_PUBLIC_CLOUDFLARE_SITE_KEY`: Public key used for Cloudflare Turnstile widget.  
`NEXT_PUBLIC_CLOUDFLARE_ENABLED`: Indicates if Cloudflare Turnstile widget is enabled
