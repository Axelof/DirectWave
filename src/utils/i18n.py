import gettext

from definitions import LOCALES_DIR, LOCALES_DOMAIN


def configure_gettext():
    gettext.install(LOCALES_DOMAIN, LOCALES_DIR)


def _(message: str):
    return gettext.gettext(message)
