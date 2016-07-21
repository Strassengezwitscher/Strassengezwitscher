# pylint: disable=bad-builtin
from __future__ import unicode_literals
from email.utils import formatdate

from django.core.mail import EmailMessage, SafeMIMEText, SafeMIMEMultipart, make_msgid
from django.core.mail.utils import DNS_NAME
from django.core.mail.backends.locmem import EmailBackend as LocMemEmailBackend
from django.utils.encoding import smart_text, force_text
from django.conf import settings
from django.core import mail

from gnupg import GPG

from strassengezwitscher.log import logger
from contact.models import Key
from contact.utils import GPGException, TemporaryDirectory, handle_gpg_error


class GPGEmailMessage(EmailMessage):
    """
    Django's default email class on paranoia.
    The email is encrypted (but not signed) during send() using GPG in PGP/MIME format.
    """
    encrypted_subtype = 'encrypted'
    gpg_attachment_filename = 'encrypted.asc'

    def _encrypt(self, plain):
        # test if we have public keys for all recipients
        available_recipients = []
        keys = []
        for key in Key.objects.all():
            keys.append(key)
            available_recipients.extend(key.addresses.split(', '))
        logger.debug("available_recipients: %s", available_recipients)
        if not all(recipient in available_recipients for recipient in self.recipients()):
            logger.error("Public key not present for at least one of these recipient: %s", self.recipients())
            raise GPGException("Public key not present for at least one recipient")

        # encryption
        with TemporaryDirectory() as temp_dir:
            gpg = GPG(gnupghome=temp_dir)
            for key in keys:
                gpg.import_keys(key.key)

            res = gpg.encrypt(plain, self.recipients(), always_trust=True)
            if not res:
                handle_gpg_error(res, 'encryption')
            return smart_text(res)

    def message(self):
        """
        Returns the final message to be sent, including all headers etc. Content and attachments are encrypted using
        GPG in PGP/MIME format (RFC 3156).
        """

        def build_plain_message():
            msg = SafeMIMEText(self.body, self.content_subtype, encoding)
            msg = self._create_message(msg)
            return msg

        def build_version_attachment():
            version_attachment = SafeMIMEText('Version: 1\n', self.content_subtype, encoding)
            del version_attachment['Content-Type']
            version_attachment.add_header('Content-Type', 'application/pgp-encrypted')
            version_attachment.add_header('Content-Description', 'PGP/MIME Versions Identification')
            return version_attachment

        def build_gpg_attachment():
            gpg_attachment = SafeMIMEText(encrypted_msg, self.content_subtype, encoding)
            del gpg_attachment['Content-Type']
            gpg_attachment.add_header('Content-Type', 'application/octet-stream', name=self.gpg_attachment_filename)
            gpg_attachment.add_header('Content-Disposition', 'inline', filename=self.gpg_attachment_filename)
            gpg_attachment.add_header('Content-Description', 'OpenPGP encrypted message')
            return gpg_attachment

        encoding = self.encoding or settings.DEFAULT_CHARSET

        # build message including attachments as it would also be built without GPG
        msg = build_plain_message()

        # encrypt whole message including attachments
        encrypted_msg = self._encrypt(str(msg))

        # build new message object wrapping the encrypted message
        msg = SafeMIMEMultipart(_subtype=self.encrypted_subtype,
                                encoding=encoding,
                                protocol='application/pgp-encrypted')

        version_attachment = build_version_attachment()
        gpg_attachment = build_gpg_attachment()
        msg.attach(version_attachment)
        msg.attach(gpg_attachment)

        self.extra_headers['Content-Transfer-Encoding'] = '7bit'

        # add headers
        # everything below this line has not been modified when overriding message()
        ############################################################################

        msg['Subject'] = self.subject
        msg['From'] = self.extra_headers.get('From', self.from_email)
        msg['To'] = self.extra_headers.get('To', ', '.join(map(force_text, self.to)))
        if self.cc:
            msg['Cc'] = ', '.join(map(force_text, self.cc))
        if self.reply_to:
            msg['Reply-To'] = self.extra_headers.get('Reply-To', ', '.join(map(force_text, self.reply_to)))

        # Email header names are case-insensitive (RFC 2045), so we have to
        # accommodate that when doing comparisons.
        header_names = [key.lower() for key in self.extra_headers]
        if 'date' not in header_names:
            msg['Date'] = formatdate()
        if 'message-id' not in header_names:
            # Use cached DNS_NAME for performance
            msg['Message-ID'] = make_msgid(domain=DNS_NAME)
        for name, value in self.extra_headers.items():
            if name.lower() in ('from', 'to'):  # From and To are already handled
                continue
            msg[name] = value

        return msg


class GPGLocMemEmailBackend(LocMemEmailBackend):
    """
    An email backend for use during test sessions.

    Emails are prepared for final sending, so they include all headers etc.

    The test connection stores email messages in a dummy outbox,
    rather than sending them out on the wire.

    The dummy outbox is accessible through the outbox instance attribute.
    """

    def send_messages(self, messages):
        """Redirect final messages to the dummy outbox"""
        messages = [message.message() for message in messages]
        mail.outbox.extend(messages)
        return len(messages)
