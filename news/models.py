import os
from datetime import datetime

from PIL import Image
from django.db import models
from django_summernote.fields import SummernoteTextField


class News(models.Model):
    """Модель новостей"""
    title = models.CharField(max_length=255,verbose_name="Заголовок")
    main_image = models.ImageField(upload_to='news_images/%Y/%m/%d/', verbose_name="Изображение к новости")
    preview_image = models.ImageField(upload_to='news_previews/%Y/%m/%d/',verbose_name="Превью-изображение" ,blank=True)
    text = SummernoteTextField()
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    author = models.CharField(max_length=255, verbose_name="Автор")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.main_image:
            try:
                today = datetime.now()
                preview_dir = os.path.join('media/news_previews/', today.strftime('%Y/%m/%d/'))
                os.makedirs(preview_dir, exist_ok=True)
                preview_path = os.path.join(preview_dir, os.path.basename(self.main_image.name))

                with Image.open(self.main_image.path) as img:
                    img.thumbnail((200, 200))
                    img.save(preview_path)

                self.preview_image = os.path.relpath(preview_path, 'media/')
                super().save(*args, **kwargs)
            except FileNotFoundError:
                print(f"Главное изображение {self.main_image.path} не найдено.")
            except Exception as e:
                print(f"Ошибка при генерации превью: {e}")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
