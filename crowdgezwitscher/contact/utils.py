from crowdgezwitscher.log import logger


class GPGException(ValueError):
    pass


# basically from: https://github.com/stephenmcd/django-email-extras/blob/master/email_extras/utils.py
def addresses_for_key(gpg_keychain, key):
    """
    Takes a key and extracts its email addresses.
    """
    fingerprint = key['fingerprint']
    addresses = []
    for key in gpg_keychain.list_keys():
        if key['fingerprint'] == fingerprint:
            # parse raw email addresses (without preceding name)
            addresses.extend([address.split('<')[-1].strip('>') for address in key['uids'] if address])
    assert len(addresses) > 0
    return addresses


def handle_gpg_error(result, operation):
    """
    Raises a generic GPG-related exception and shows additional information if available.
    """
    log_msg = "GPG %s failed." % operation
    # log additional helpful attributes which are not always present
    for attr in ['status', 'stderr']:
        if hasattr(result, attr):
            log_msg += "\n%s: %s" % (attr, getattr(result, attr))
    logger.error(log_msg)
    raise GPGException("GPG operation failed")
