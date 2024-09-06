from django.db import models
from django.urls import reverse


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )
    url = models.CharField(max_length=200, blank=True, null=True)
    named_url = models.CharField(max_length=200, blank=True, null=True)
    menu_name = models.CharField(max_length=100)

    def get_absolute_url(self):
        if self.named_url:
            return reverse(self.named_url)
        return self.url

    def __str__(self):
        return self.name

    def get_ancestors(self):
        """Возвращает всех предков текущего элемента"""
        ancestors = []
        parent = self.parent
        while parent:
            ancestors.append(parent)
            parent = parent.parent
        return ancestors

    def get_descendants(self):
        """Возвращает всех потомков текущего элемента"""
        descendants = []
        for child in self.children.all():
            descendants.append(child)
            descendants.extend(child.get_descendants())
        return descendants

    class Meta:
        verbose_name = "Меню"
        verbose_name_plural = "Меню"
