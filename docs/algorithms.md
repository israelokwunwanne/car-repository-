# Key Process Algorithms

These steps describe the current application behavior and should be used when preparing matching test cases.

## Registration

1. If the visitor is already authenticated, redirect to the home page.
2. Validate username/password with Django's `UserCreationForm` rules and validate email uniqueness without regard to case.
3. If invalid, redisplay the form with field errors.
4. Save the user; the account signal creates a profile, then store the submitted phone number on that profile.
5. Log in the new user, show a welcome message, and redirect home.

## Login And Logout

1. Submit credentials to Django's `LoginView`.
2. If credentials are valid, establish the authenticated session and follow Django's configured redirect behavior.
3. For admin login, accept the session only when the authenticated user has `is_staff=True`; otherwise show an access error.
4. Logout is a POST action, clears the session, and redirects home.

## Booking Request

1. Require an authenticated customer; guests are redirected to login.
2. Offer only vehicles with `is_available=True` in the booking form.
3. Validate dates: return must be after pickup, pickup cannot be in the past, and the vehicle must be available for new requests.
4. Reject a date range that overlaps a Pending or Confirmed booking for the same vehicle. Back-to-back ranges are allowed; Cancelled bookings are ignored.
5. Set the customer from the session and status to Pending; calculate total price as rental days multiplied by the vehicle's daily price.
6. Save and redirect to a confirmation page scoped to that customer.

## Admin Confirm Or Cancel Booking

1. Require staff access and accept only the `confirm` or `cancel` action for a Pending booking.
2. Set the status to Confirmed or Cancelled and save.
3. Reject attempts to change bookings that are no longer Pending; return to booking management with a message.

## Testimonials

1. Require an authenticated user to submit a message.
2. Save it with the session user and `is_active=False`.
3. Staff review and activate it through Django admin.
4. Public listing queries only active testimonials and paginates the results.

## Vehicle Management And Catalogue

1. Staff create or edit brands and vehicles in Django admin; feature status and availability can also be changed in the list.
2. A brand with vehicles cannot be deleted until those vehicles are reassigned or deleted.
3. For public listing requests, validate optional brand, minimum/maximum price, seats, and availability filters.
4. Apply valid filters, order by brand and vehicle name, and paginate nine results per page. Invalid filter input leaves the unfiltered catalogue intact and displays validation errors.
5. Public detail pages show the selected vehicle. An available vehicle links to booking creation, where authentication is enforced by the booking flow.
6. The home page shows up to six vehicles marked featured and available.

## Contact, Subscription, And Site Content

1. Validate contact form name, email, subject, and message; save valid messages for staff review in admin, otherwise redisplay errors.
2. Validate subscriber email and save it once; the database unique constraint prevents duplicate addresses.
3. Staff edit the single site-content record in admin to change home copy and published contact information. Contact submissions and subscribers are separately searchable and manageable there.