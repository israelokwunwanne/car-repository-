# Car Rentals E-R Diagram

This diagram reflects the current Django models and their deletion rules. The built-in Django user is shown as `User`.

```mermaid
erDiagram
    USER ||--|| PROFILE : has
    USER ||--o{ BOOKING : requests
    USER ||--o{ TESTIMONIAL : writes
    BRAND ||--o{ VEHICLE : groups
    VEHICLE ||--o{ BOOKING : reserved_for

    USER {
        int id PK
        string username UK
        string email
        string password_hash
        boolean is_staff
    }
    PROFILE {
        int id PK
        int user_id FK,UK
        string phone
        string address
    }
    BRAND {
        int id PK
        string name UK
    }
    VEHICLE {
        int id PK
        int brand_id FK
        string name
        decimal price_per_day
        int seats
        string fuel_type
        string image_url
        text description
        boolean is_available
        boolean is_featured
    }
    BOOKING {
        int id PK
        int customer_id FK
        int vehicle_id FK
        date pickup_date
        date return_date
        string location
        decimal total_price
        string status
        datetime created_at
    }
    TESTIMONIAL {
        int id PK
        int user_id FK
        text message
        boolean is_active
        datetime created_at
    }
    CONTACT {
        int id PK
        string name
        string email
        string subject
        text message
        boolean is_read
        datetime created_at
    }
    SUBSCRIBER {
        int id PK
        string email UK
        boolean is_active
        datetime created_at
    }
    SITE_CONTENT {
        int id PK
        string home_heading
        text home_intro
        string contact_email
        string contact_phone
        string contact_address
        datetime updated_at
    }
```

## Keys And Relationship Rules

- `Profile.user_id` is unique: a user has one profile. Deleting the user deletes the profile.
- `Booking.customer_id` and `Booking.vehicle_id` are foreign keys. Deleting a user or vehicle deletes their bookings.
- `Testimonial.user_id` is a foreign key. Deleting a user deletes their testimonials.
- `Vehicle.brand_id` is protected while vehicles reference a brand. Remove or reassign its vehicles before deleting a brand.
- Brand names and subscriber email addresses are unique.
- Contact messages, subscribers, and editable site content are independent records and have no user foreign key.
- A booking's return date must be later than its pickup date. Pending and confirmed bookings cannot overlap for the same vehicle; cancelled bookings do not block dates.

The vehicle image is stored as a URL string (`Vehicle.image`), so this schema does not require file-storage infrastructure.

## Module Coordination

The booking module depends on `Vehicle.price_per_day` and `Vehicle.is_available`, and on the stable `Brand -> Vehicle` relation. Keep those names and meanings in sync when changing either module. The account and testimonial modules depend on Django's configured user model. Confirm relationship or deletion-policy changes with the booking/account owners before applying migrations.