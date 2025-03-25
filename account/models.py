from django.db import models


class BlacklistToken(models.Model):
    token = models.CharField(max_length=255)

    def __str__(self):
        return self.token

    class Meta:
        app_label = "account"
        db_table = "blacklist_token"
