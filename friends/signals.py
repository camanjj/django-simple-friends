from django.dispatch import Signal


friendship_accepted = Signal()


friendship_declined = Signal()


friendship_cancelled = Signal()


def create_friendship_instance(sender, instance, created, raw, **kwargs):
    from friends.models import Friendship
    if created and not raw:
        Friendship.objects.create(user=instance)


def create_userblocks_instance(sender, instance, created, raw, **kwargs):
    from friends.models import UserBlocks
    if created and not raw:
        UserBlocks.objects.create(user=instance)


def create_friendship_instance_post_syncdb(sender,
                                           app,
                                           created_models,
                                           verbosity,
                                           **kwargs):
    from django.conf import settings
    from friends.models import Friendship
    created = 0
    print "Creating friendships"
    if settings.AUTH_USER_MODEL in created_models:
        for user in settings.AUTH_USER_MODEL.objects.filter(friendship__isnull=True):
            Friendship.objects.create(user=user)
            created += 1
            if verbosity >= 2:
                print "Friendship created for %s" % user
    if verbosity >= 1:
        print "%d friendships created" % created


def create_userblock_instance_post_syncdb(sender,
                                          app,
                                          created_models,
                                          verbosity,
                                          **kwargs):
    from django.conf import settings
    from friends.models import UserBlocks
    created = 0
    print "Creating user blocks"
    if settings.AUTH_USER_MODEL in created_models:
        for user in settings.AUTH_USER_MODEL.objects.filter(user_blocks__isnull=True):
            UserBlocks.objects.create(user=user)
            created += 1
            if verbosity >= 2:
                print "User block created for %s" % user
    if verbosity >= 1:
        print "%d user blocks created" % created
