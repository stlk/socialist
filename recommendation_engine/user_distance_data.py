import logging
import itertools

from django.contrib.auth.models import User
from instagram.bind import InstagramAPIError

from .models import UserAggregation
from .instagram import Instagram


class UserDistanceData(Instagram):

    def __init__(self, user: User):
        self.user = user
        super(UserDistanceData, self).__init__(user)

    def get_recent_media(self, user_id):
        media = []
        self.log_ratelimit()
        try:
            recent_media, next_ = self.api.user_recent_media(user_id=user_id)
            media.extend(recent_media)
            while next_ and len(media) < 300:
                recent_media, next_ = self.api.user_recent_media(with_next_url=next_)
                media.extend(recent_media)
                self.log_ratelimit()
        except InstagramAPIError as e:
            if e.error_type == 'APINotAllowedError':
                logging.info("User {0} is not allowed".format(user_id))
            else:
                raise

        return media

    def get_user_data(self, user_id):
        recent_media = self.get_recent_media(user_id)
        text = ' '.join([(m.caption.text if m.caption else '') for m in recent_media])
        tags = list(itertools.chain([[t.name for t in m.tags] for m in recent_media if m.tags]))
        return UserAggregation(
            raw_text=text,
            tags=tags,
            user_id=user_id,
            media_count=len(recent_media),
            username=recent_media[0].user.username)

    def get_user_aggregations(self, users):
        # Load data for current user, so we have something we can compare to.
        users = list(users)
        users.append(self.user.social_auth.get().uid)

        for user_id in users:
            if UserAggregation.objects.filter(user_id=user_id).exists():
                logging.info('Skipping... %s', user_id)
            else:
                user_data = self.get_user_data(user_id)
                user_data.save()
                logging.info('Saving... %s', user_id)
