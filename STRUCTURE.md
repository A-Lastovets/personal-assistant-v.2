+---personal_assistant
|   .env
|   .env.sample
|   .gitignore
|   dockerfile
|   LICENSE
|   poetry.lock
|   pyproject.toml
|   README.md
|   requirements.txt
|
+---personal_assistant
|   |   manage.py
|   
+---contacts_app
|   |   __init__.py
|   |   admin.py
|   |   apps.py
|   |   forms.py
|   |   models.py
|   |   tests.py
|   |   urls.py
|   |   views.py
|   +---migrations
|   |       __init__.py
|           
+---files_app
|   |   __init__.py
|   |   admin.py
|   |   apps.py
|   |   forms.py
|   |   models.py
|   |   tests.py
|   |   urls.py
|   |   views.py
|   +---migrations
|   |       __init__.py
| 
+---media
|   |
|   +---profile_images
|  
+---news_app
|   |   __init__.py
|   |   admin.py
|   |   apps.py
|   |   models.py
|   |   tests.py
|   |   urls.py
|   |   views.py
|   +---migrations
|   |       __init__.py
|           
+---notes_app
|   |   __init__.py
|   |   admin.py
|   |   apps.py
|   |   forms.py
|   |   models.py
|   |   tests.py
|   |   urls.py
|   |   views.py
|   +---migrations
|           __init__.py
|   +---templatetags
|       notes_custom_filters.py
|
+---users_app
|   |   __init__.py
|   |   admin.py
|   |   apps.py
|   |   forms.py
|   |   models.py
|   |   signals.py
|   |   tests.py
|   |   urls.py
|   |   views.py
|   +---migrations
|   |       __init__.py
|   +---templatetags
|       custom_filters.py
|
+---personal_assistant
|   |   asgi.py
|   |   settings.py
|   |   urls.py
|   |   views.py
|   |   wsgi.py
|   |   __init__.py
|   
+---templates
|   |   base.html
|   |   home.html
|   |   news.html
|   +---contacts_app
|   |       add_contact.html
|   |       contact_detail.html
|   |       contact_home.html
|   |       contact_list.html
|   |       contact_search.html
|   |       edit_contact.html
|   |       upcoming_birthdays.html
|   +---files_app
|   |       file_list.html
|   |       upload.html
|   +---notes_app
|   |       add_note.html
|   |       edit_note.html
|   |       note_detail.html
|   |       note_home.html
|   |       note_list.html
|   +---users
|           login.html
|           password_reset_complete.html
|           password_reset_confirm.html
|           password_reset_done.html
|           password_reset_email.html
|           password_reset_subject.txt
|           password_reset.html
|           profile.html
|           signup.html
|           
+---static
|   |   style.css
|   |   paginations.css
|   +---contacts_app
|   |       add_contact.css
|   |       contact_list.css
|   +---files_app
|   |       files_app.css
|   |       audio_placeholder.png
|   |       doc_placeholder.png
|   |       image_placeholder.png
|   |       video_placeholder.png
