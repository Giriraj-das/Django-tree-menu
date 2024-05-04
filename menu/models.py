from django.db import models


class MenuName(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Menu(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    menu_name = models.ForeignKey(MenuName, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
