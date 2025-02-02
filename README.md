# FAQ API

## Installation
1. Clone the repository:

git clone <repo_url>
cd faq_project

2. Create a virtual environment:

python3 -m venv env
source env/bin/activate

3. Install dependencies:

pip install -r requirements.txt

4. Run the server:

python3 manage.py runserver

## API Usage
- Fetch FAQs (default: English):

curl http://localhost:8000/api/faqs/

- Fetch FAQs in Hindi:

curl http://localhost:8000/api/faqs/?lang=hi

- Fetch FAQs in Bengali:

curl http://localhost:8000/api/faqs/?lang=bn

## Deployment
- Docker support available.
