import logging
from functools import reduce
from collections import Counter

from django.contrib.auth.models import User
from instagram.bind import InstagramAPIError

from .collections import unique
from .models import UserAggregation
from .instagram import Instagram


def retreive_tags(result, tags):
    result += list(map(lambda tag: tag.name, tags))
    return result


def weight_by_tags(weights, tags):
    weight = 1
    for tag in tags:
        tag_weight = [w[1] for w in weights if w[0] == tag]
        weight += (1 if len(tag_weight) == 0 else tag_weight[0]) * 0.01
    return weight


def keep_only_images(collection):
    return filter(lambda m: m.type == 'image', collection)


def photo_dictionary(m, top_10_tags_with_count):
    tags = list(map(lambda t: t.name, m.tags))
    return {
        'id': m.id,
        'user_id': m.user.id,
        'username': m.user.username,
        'caption': (m.caption.text if m.caption else ''),
        'likes': m.like_count,
        'comments': m.comment_count,
        'link': m.link,
        'url': m.get_standard_resolution_url(),
        'tags': tags,
        'tag_weight': weight_by_tags(top_10_tags_with_count, tags)
    }


class RelatedPhotos(Instagram):

    def __init__(self, user: User):
        self.user = user
        super(RelatedPhotos, self).__init__(user)

    def get_liked_media(self):
        media = []
        self.log_ratelimit()
        liked_media, next_ = self.api.user_liked_media()
        media.extend(liked_media)
        while next_:
            liked_media, next_ = self.api.user_liked_media(with_next_url=next_)
            media.extend(liked_media)
            self.log_ratelimit()
        return media

    def get_media_for_tag(self, tag):
        media = []
        self.log_ratelimit()
        try:
            tag_recent_media, next_ = self.api.tag_recent_media(tag_name=tag)
            media.extend(tag_recent_media)
            while next_ and len(media) < 200:
                tag_recent_media, next_ = self.api.tag_recent_media(tag_name=tag,
                                                                    with_next_url=next_)
                media.extend(tag_recent_media)
                self.log_ratelimit()
        except InstagramAPIError as e:
            if e.error_type == 'APINotAllowedError':
                logging.info("Tag {0} is not allowed".format(tag))
            else:
                raise
        return media

    def get_top_10_tags(self):
        media = self.get_liked_media()

        tags_collections = map(lambda photo: photo.tags, media)
        tags_collections = reduce(retreive_tags, tags_collections, [])

        top_10_tags_with_count = Counter(tags_collections).most_common(10)
        top_10_tags = map(lambda tag: tag[0], top_10_tags_with_count)
        return top_10_tags, top_10_tags_with_count

    def find_media_for_tag(self, tag):
        aggregations = UserAggregation.objects.filter(tags__contains=[tag])
        if aggregations.exists():
            user_id = aggregations[0].user_id
            logging.info("Loading tag {0} for user {1}...".format(tag, user_id))
            recent_media, next_ = self.api.user_recent_media(user_id=user_id)
            return recent_media
        else:
            logging.info("Loading tag... {0}".format(tag))
            return self.get_media_for_tag(tag)

    def recommend(self):
        top_10_tags, top_10_tags_with_count = self.get_top_10_tags()

        media_for_user = []
        for tag in top_10_tags:
            media_for_user.extend(keep_only_images(self.find_media_for_tag(tag)))

        media_for_user_processed = map(lambda m: photo_dictionary(m, top_10_tags_with_count), media_for_user)
        media_for_user_processed = unique(media_for_user_processed, lambda m: m['id'])

        media_for_user_processed = sorted(media_for_user_processed,
                                          key=lambda m: m['tag_weight'],
                                          reverse=True)
        return list(media_for_user_processed)
