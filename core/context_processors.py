def site_settings(request):
    """Global template variables available on every page."""
    return {
        'SITE_NAME': 'Smart Garage',
        'SITE_TAGLINE': 'Premium Vehicle Service, Simplified.',
    }
