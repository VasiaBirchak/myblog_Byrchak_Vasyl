from rest_framework.response import Response
from rest_framework import status
from django.contrib.contenttypes.models import ContentType
from django.db.models import F
from blog.models import Like


class LikeModelMixin:
    @staticmethod
    def like_action(obj, user):
        content_type = ContentType.objects.get_for_model(obj)
        like, created = Like.objects.get_or_create(user=user,
                                                   content_type=content_type,
                                                   object_id=obj.id)
        # if created:
        #     obj.likes_count = F('likes_count') + 1
        #     obj.save(update_fields=['likes_count'])
        #     obj.refresh_from_db(fields=['likes_count'])
        #     return Response({'status': 'liked',
        #                     'likes_count': obj.likes_count}, status=status.HTTP_201_CREATED)
        # return Response({'status': 'already liked',
        #                 'likes_count': obj.likes_count}, status=status.HTTP_200_OK)
        if created:
            return Response({'status': 'liked', 'likes_count': obj.likes_count}, status=status.HTTP_201_CREATED)
        return Response({'status': 'already liked', 'likes_count': obj.likes_count}, status=status.HTTP_200_OK)

    @staticmethod
    def unlike_action(obj, user):
        content_type = ContentType.objects.get_for_model(obj)
        deleted, _ = Like.objects.filter(user=user,
                                         content_type=content_type, object_id=obj.id).delete()
        # if deleted:
        #     obj.likes_count = F('likes_count') - 1
        #     obj.save(update_fields=['likes_count'])
        #     obj.refresh_from_db(fields=['likes_count'])
        #     return Response({'status': 'unliked',
        #                     'likes_count': obj.likes_count}, status=status.HTTP_200_OK)
        # return Response({'status': 'not liked',
        #                 'likes_count': obj.likes_count}, status=status.HTTP_200_OK)
        return Response({'status': 'unliked', 'likes_count': obj.likes_count}, status=status.HTTP_200_OK)