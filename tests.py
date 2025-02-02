import pytest
from django.urls import reverse
from .models import FAQ

@pytest.fixture
def create_faq(db):
    def _create_faq(question, answer):
        return FAQ.objects.create(question=question, answer=answer)
    return _create_faq

@pytest.mark.django_db
def test_faq_model(create_faq):
    faq = create_faq(question="What is your name?", answer="My name is Bard.")
    assert faq.question == "What is your name?"
    assert faq.question_hi is not None  # Check if Hindi translation is populated
    assert faq.get_translated_text('question', 'hi') == faq.question_hi

@pytest.mark.django_db
def test_faq_list_api(client, create_faq):
    create_faq(question="English Question", answer="English Answer")

    # Test English
    response = client.get(reverse('faq_list'))
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['question'] == "English Question"

    # Test Hindi
    response = client.get(reverse('faq_list') + '?lang=hi')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['question'] == FAQ.objects.first().question_hi