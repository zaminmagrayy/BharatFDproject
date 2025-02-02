from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import FAQ
from .serializers import FAQSerializer
from django.core.cache import cache

@api_view(['GET'])
def faq_list(request):
    lang = request.query_params.get('lang', 'en')  # Default to English
    cache_key = f'faq_{lang}'

    faqs = cache.get(cache_key)
    if faqs is None:
        faqs = FAQ.objects.all()
        serialized_faqs = []
        for faq in faqs:
            serialized_faq = {
                'id': faq.id,
                'question': faq.get_translated_text('question', lang),
                'answer': faq.get_translated_text('answer', lang)
            }
            serialized_faqs.append(serialized_faq)

        cache.set(cache_key, serialized_faqs, timeout=300) # Cache for 5 minutes
    else:
        serialized_faqs = faqs

    return Response(serialized_faqs)