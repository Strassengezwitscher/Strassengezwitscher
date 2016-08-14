class NoStaffMixin(object):
    """
    This mixin is to be used for Django's class based views for the User model.
    By including it as a base class before the actual view class, the mixin assures that staff users (those able to
    log in to Django's admin UI) cannot be accessed. This helps seperating these users from those that can log in to the
    internal area of the platform.
    """

    def get_queryset(self):
        return super(NoStaffMixin, self).get_queryset().exclude(is_staff=True)
