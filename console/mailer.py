from django.conf import settings
import sendwithus

class Mailer():

    def __init__(self):
        self.api = sendwithus.api(api_key=settings.SENDWITHUS_KEY)

    def send_recommendations(self, email, photos):
        r = self.api.send(
            email_id=settings.SENDWITHUS_TEMPLATE,
            recipient={'address': email},
            sender={'name': 'socialist.', 'address':'socialist@post.rousek.name'},
            email_data={'photos': photos})
        print(r.status_code)
