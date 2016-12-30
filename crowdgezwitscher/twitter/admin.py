from django.contrib import admin

from twitter.models import TwitterAccount, Hashtag, Tweet


admin.site.register(TwitterAccount)
admin.site.register(Hashtag)
admin.site.register(Tweet)
