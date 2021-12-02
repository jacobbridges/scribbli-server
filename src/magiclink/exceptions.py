class MagicLinkError(Exception):
    """Top level exception in the MagicLink module."""
    pass


class MagicLinkMissingRequiredParamsError(MagicLinkError):
    """Missing token or email in the authentication call."""
    pass


class MagicLinkNotFoundError(MagicLinkError):
    """No magic link could be found matching the criteria."""
    pass


class MagicLinkExpiredError(MagicLinkError):
    """Magic link expired."""
    pass


class MagicLinkForDeactivatedUserError(MagicLinkError):
    """Magic link is associated to a deactivated account."""
    pass
