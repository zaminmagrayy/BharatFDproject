from django.db import models
from ckeditor.fields import RichTextField
from googletrans import Translator
from django.core.cache import cache

class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField()
    question_hi = models.TextField(blank=True, null=True)
    answer_hi = models.TextField(blank=True, null=True)
    question_bn = models.TextField(blank=True, null=True)
    answer_bn = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Automatic translation
        translator = Translator()
        self.question_hi = self.translate_text(self.question, 'hi')
        self.answer_hi = self.translate_text(self.answer, 'hi')
        self.question_bn = self.translate_text(self.question, 'bn')
        self.answer_bn = self.translate_text(self.answer, 'bn')

        # Invalidate cache for all languages
        cache.delete('faq_en')
        cache.delete('faq_hi')
        cache.delete('faq_bn')

        super().save(*args, **kwargs)

    def translate_text(self, text, dest_lang):
        cache_key = f'translation:{text}:{dest_lang}'
        translated_text = cache.get(cache_key)

        if translated_text is None:
            translator = Translator()
            try:
                translated_text = translator.translate(text, dest=dest_lang).text
            except Exception as e:
                print(f"Translation error: {e}")
                translated_text = text  # Fallback to original text

            cache.set(cache_key, translated_text, timeout=3600)  # Cache for 1 hour

        return translated_text

    def get_translated_text(self, field, lang):
        translated_field = f"{field}_{lang}"
        return getattr(self, translated_field, getattr(self, field))

    def __str__(self):
        return self.question