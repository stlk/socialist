from django.contrib.auth.models import User

from recommendation_engine.instagram import Instagram


class Instagram(Instagram):

    def __init__(self, user: User):
        super(Instagram, self).__init__(user)

    def user_has_no_posts(self):
        self.log_ratelimit()
        user = self.api.user()
        return user.counts['media'] == 0
