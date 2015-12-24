import logging

from .models import UserAggregation
from .instagram import Instagram


class UserDistanceData(Instagram):

    def get_recent_media(self, user_id):
        media = []
        self.log_ratelimit()
        recent_media, next_ = self.api.user_recent_media(user_id=user_id)
        media.extend(recent_media)
        while next_ and len(media) < 200:
            recent_media, next_ = self.api.user_recent_media(with_next_url=next_)
            media.extend(recent_media)
            self.log_ratelimit()
        return media

    def get_user_data(self, user_id):
        recent_media = self.get_recent_media(user_id)
        text = ' '.join([(m.caption.text if m.caption else '') for m in recent_media])
        return UserAggregation(
            raw_text=text,
            user_id=user_id,
            media_count=len(recent_media),
            username=recent_media[0].user.username)

    def get_user_aggregations(self, users):
        for user_id in users:
            if UserAggregation.objects.filter(user_id=user_id).exists():
                logging.info('Skipping... %s', user_id)
            else:
                user_data = self.get_user_data(user_id)
                user_data.save()
                logging.info('Saving... %s', user_id)
