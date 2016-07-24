from django.conf import settings

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import authentication_classes, api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

from strassengezwitscher.log import logger
from strassengezwitscher.auth import CsrfExemptSessionAuthentication
from contact.forms import ContactForm
from contact.mail import GPGEmailMessage
from contact.utils import GPGException

EMAIL_TEMPLATE = """
Nachricht von: %s
Email-Adresse: %s
Betreff: %s
Autor ist Journalist: %s
Nachricht ist vertraulich: %s
Nachricht:

%s
"""


@api_view(['POST'])
@authentication_classes((CsrfExemptSessionAuthentication,))
@parser_classes((MultiPartParser, FormParser,))
def send_form(request):
    """
    Receives data from a contact form and creates a GPG-encrypted email including that data.
    Depending on the data's given confidentiality the email is sent to pre-defined receivers.
    """
    form = ContactForm(request.POST, request.FILES)
    if not form.is_valid():
        return Response({'status': 'error', 'errors': form.errors},
                        status=status.HTTP_400_BAD_REQUEST)

    data = form.cleaned_data
    uploaded_files = request.FILES.getlist('files')
    if uploaded_files:
        res = form.files_are_valid(request)
        if res is not True:
            return Response({'status': 'error', 'errors': res},
                            status=status.HTTP_400_BAD_REQUEST)
        logger.debug("Contact data includes %i uploaded file(s).", len(uploaded_files))

    subject = "Neue Nachricht von Streetcoverage"

    body = EMAIL_TEMPLATE % (
        data['name'] or "(kein Name angegeben)",
        data['email'] or "(keine Emailadresse angegeben)",
        data['subject'],
        "ja" if data['journalist'] else "nein",
        "ja" if data['confidential'] else "nein",
        data['message']
    )

    if data['confidential']:
        receivers = settings.EMAIL_TO_CONTACT_CONFIDENTIAL
    else:
        receivers = settings.EMAIL_TO_CONTACT_NON_CONFIDENTIAL

    email = GPGEmailMessage(subject, body, settings.EMAIL_FROM_CONTACT, receivers)

    for uploaded_file in uploaded_files:
        # uploaded_file is an InMemoryUploadedFile created by MemoryFileUploadHandler (see setting
        #    FILE_UPLOAD_HANDLERS). Its mode includes 'b' so its content is a byte string.
        # Django's attach functionality internally invokes encode() when the file consists of text.
        # Byte strings however do not have an encode() method, so we decode the byte string to a normal string.
        # Alternative: instead of attach() we could use attach_file() which has been made aware of types:
        #   https://github.com/django/django/commit/c6da621def9bc04a5feacd5652c7f9d84f48ad2c
        # This would require writing the uploaded file to disk, e.g. using method().
        # Note that TemporaryUploadedFile created by TemporaryFileUploadHandler does write files to disk, but uses
        #   tempfile.NamedTemporaryFile's default mode 'w+b', so we could create a subclass of both classes as
        # another alternative.
        if uploaded_file.content_type and uploaded_file.content_type.split('/')[0] == 'text':
            email.attach(uploaded_file.name, uploaded_file.read().decode(),)
        else:
            email.attach(uploaded_file.name, uploaded_file.read(),)

    try:
        email.send()
        logger.info("Contact email has been sent.")
    except GPGException:
        return Response({'status': 'error', 'errors': 'Email could not be sent.'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'status': 'success'})
