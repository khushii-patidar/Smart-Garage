# Smart Garage — Phase 1

## Run locally
```
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Test login (Owner): username `owner`, password `garage@123`
Admin panel: /admin/

## What's in Phase 1
- Project scaffold with 9 apps: accounts, customers, bookings, jobcards, inventory, billing, reports, notifications, core
- Custom User model with roles (OWNER / ADVISOR / MECHANIC / CUSTOMER) + MechanicProfile + AdvisorProfile
- SQLite database, DRF + JWT installed and configured (endpoints wired from Phase 4 onward)
- Auth: login, customer self-registration, logout
- Role-based dashboard redirect + 4 dashboard shells (sidebar layout)
- Design system: static/css/design-system.css (color tokens, typography, buttons, cards, forms, toasts, dashboard shell)
- Shared JS: static/js/core.js (toasts, scroll-reveal, animated counters, sidebar toggle, API fetch helper)
- Placeholder landing page (full version = Phase 2)

## Next: Phase 2 — full long-scroll landing page
