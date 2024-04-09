# LEADS ENGINE

### Introduction:

#### A lead generation system that helps small businesses and startups:

Leads is a lead generation app built using Django 4.1.7. It helps small businesses and startups convert their website visitors into **qualified** leads.

How does it do this? In internet marketing, a _lead magnet_ is a small token of goodwill that is offered to website visitors in order to collect their email address. These are normally some kind of PDF or document, perhaps an ebook or a free report. These days, video tutorials and short term courses are also given away.

**Leads** takes this a step further. Instead of asking the user for their email and offering just another resource, Leads asks the visitor to _participate in a quiz, or survey_ of some sorts, and based on their responses, offers to send a _personalized PDF report_ to their email address. In essence, Leads allows small business and startups to:

- conduct market research by asking relevant questions in the survey
- classify leads according to conversion potential, based on their survey responses
- offer a personalized lead magnet to build authority
- build an email list of qualified, warm leads
- visualize and analyze survey responses to make informed business decisions

### Distinctiveness and Complexity:

#### Distinctiveness

Getting visitors to your website is a hard enough task. Businesses use many tactics such as content marketing, influencer marketing and paid ads to somehow get visitors to their website. But what next?

More often than not, visitors aren't going to be purchasing any product or service from a website they've barely heard of, especially during their first visit. And even if the site looks really cool, even if they _bookmark_ the site, the chances of them coming back is **almost nil**. So that brings up an important question.

**How do we get the attention of our hard-earned visitors?**

Giving _just anything_ away for free no longer seems to work in the internet landscape these days - partly due to increased competition among businesses, but most importantly due to the **limited attention span** of web users. Most users recognize _lead magnets_ instantly, and sense an upsell.

It is often easier to onboard visitors through an _interactive process_, and that is the aim of this project.

Leads as a project is believed to be unique and sufficiently distinct from any other project in the CS50W course. It aims to solve the real-world problem of **lead generation** - converting website visitors into qualified leads, a common issue faced by solo entrepreneurs, small businesses and startups.

It consists of a simple **squeeze page** that highlights in a crisp and clear manner what the _value proposition_ of the business is. A _personalized PDF report_ is the lead magnet being offered, but instead of directly asking the visitor to type their email address on an unknown website, Leads reduces the friction by asking them to take part in a _quick survey_.

This survey is important and the questions should be designed to highlight the pain points/desires of the target audience. If done correctly, as the prospect moves through the survey, one question a time, they will be able to resonate with the business, and will provide their email address to get that personalized PDF report in their inbox!

Businesses can then analyze the survey data and get valuable insights to build or tweak their products and services.

#### Complexity

Although the user interface of Leads has deliberately been kept simple and minimal (I admit that it looks ugly), and contains just more than a couple of pages, there is a reasonable level of complexity involved in the project.

The Django project called Leads contains just a single app called Survey. Survey is based on **5 data models** - _Lead_, _Survey_, _Question_, _Response_ and _Answer_, that connect well with each other to allow a seamless quiz experience.

The project is mostly Python and Django templates, styled with Bootstrap, with a bit of Javascript code to enhance interactivity. Below are some of the key aspects with respect to the project's complexity:

###### Database design

Determining the exact number of models and how the models should relate to one another was a time-consuming trial-and-error process.

###### Multiple question types

Questions in the survey can be _descriptive_, _multiple choice with a single answer_, or _multiple choice with multiple answers_.

###### Lead scoring system

A _score_ is generated for every lead that takes the survey. The scoring system is fairly straightforward and **completely opinionated**. It is based solely on the _multiple choice with multiple answers_ type of questions. These questions should typically reveal important pain points of the target audience, and ask them to select all which apply. Every visitor starts with a full score, and as the user selects pain points (answers), the lead's score goes down. The foundational principle of the scoring system is:
**Lower the score, higher the prospect's need for a solution**

###### Quiz single-page-application

To provide a more interactive experience for the user, the quiz shows only one question at a time, with the ability to toggle between questions at any time. This was implemented using Javascript. Responses are server validated and duplicate surveys by the same lead are not allowed.

###### Personalized PDF report generation

Once a visitor completes a survey and their score is generated, a personalized PDF report is generated using the ReportLab library. Since ReportLab is not _thread-safe_, the single thread is *lock*ed using Python's threading module. This prevents possible weird behavior when multiple requests to generate PDF are sent to the server.

###### Emailing system

The generated PDF is attached and mailed to the lead, using Django's built-in email system. To store sensitive data, such as email account host and password, the _python-decouple_ 3rd party library was used, and this allows to store the above as environment variables in the project's root inside a _.env_ file.

###### Basic survey insights

The survey responses for each question is visualized in an admin-only view that is accessible to superusers via the Django admin. The 3rd party library _Plotly_ was used for generating pie charts.

###### Customized Django admin

Making survey insights accessible for superuser-only forced a peek through the **Django source code** to find and modify the right templates. Admin views for multiple models where tweaked by adding _inline models_.

### Project Documentation:

###### The project uses Django 4.1.7 and Python 3.10.6, was bootstrapped with the `django-admin startproject` command in a Python virtual environment (venv) and contains a single app called `survey`.

3rd party libraries were added to a `requirements.txt` file using `pip freeze`.

The major 3rd party libraries (dependencies excluded) used are:

- ReportLab
- Plotly
- Python-Decouple
- Black (code formatter)

**The project has just one `templates` and `static` folders in the root directory, rather than one each in every app. This was thought to be more convenient (opinionated).**

UI design was the least of focuses for this project and a very minimal design was build using **Bootstrap 5.3.2** (acquired via CDN). Since custom CSS was not written, it has not been linked to the templates. An empty `base.css` file has, nevertheless, been kept inside the project.

##### Folders and files documentation

###### `leads` folder

This folder contains the project `settings.py` file and `urls.py`.

- `settings.py` was modified, in order to add settings for the _email backend_, root `templates` and `static` directories, to add the `survey` app to `INSTALLED_APPS`.
- `urls.py` was modified to `include` the `survey` app's URLs.
- `asgi.py` and `wsgi.py` were not modified. They seem to contain configuration settings for ASGI and WSGI gateways.

###### `static` folder

The static folder should contain all the static files, CSS and JS for this project. At present, it contains an empty `base.css` file for custom styles in a `css` folder, and a `quiz.js` file that contains the code for making the quiz interactive, in the `js` folder.

- The `quiz.js` file has Javascript functions that allow showing one question at a time, and for toggling back and forth between questions.

###### `survey` folder

This is the main `survey` app folder which contains the core logic of the project. The `migrations` folder contains the versions of `migrations` applied.

- `admin.py` contains the code for registering models to the Django admin site. `ModelAdmin` classes were modified for `Survey` and `Question` models, and `InlineModels` added for `Response` and `Answer` models. This was done to make data access easy. The site header was renamed to `Leads Administration`.
- `apps.py` was not modified. It contains an instance of the class that would be included in `INSTALLED_APPS = [...]` in `settings.py`.
- `models.py` contains all 5 database models of our application - `Lead`, `Survey`, `Question`, `Response` and `Answer`. Custom methods such as `get_questions()`, `get_lead()` and `get_answer_options` were written. Not all of them came in handy, but have been kept, should they be required in future.
- `tests.py` should contain the tests for our views and models, but have not been implemented(yet) due to them not being a hard requirement, but primarily due to time constraints. Their importance is nevertheless, understood.
- `urls.py` contains the URLs for our views, which are just 3 - a `HomePageView` that is generic class-based `TemplateView`, a class-based `QuizView` which has both `get()` and `post()` functions defined for retrieving and submitting the form, respectively. Finally, there is a function-based view `analyze` that is restricted by the `staff_member_required` decorator. This is for admins to view insights from the survey responses. This view can be accessed from the Leads administration site.
- `utils.py` contains utility functions that help us `calculate_score` for the `lead`, `generate_report` to generate the personalized PDF report based on `lead.score` and `mail_report` to send the mail with report in the attachments. The `threading.Lock()` for `reportlab`'s thread-safety issue was implemented here.
- `views.py` contains the code for our 3 views. `HomePageView` renders the welcome homepage. `QuizView` has a `get()` function that retrieves the quiz questions and answers, and a `post()` function to submit the form. `QuizView` is responsible for all the resource creation. The resource creation process can be briefed as follows: first, a check is made if all responses were filled. If so, new `lead` and `survey` resources are created. If a `lead` with the same email already exists in the database, an error page is displayed. If things go well, several `responses` are created and the 3 `utils.py` functions - `utils.calculate_score()`, `utils.generate_report()` and `utils.mail_report` are called. Finally, the visitor is shown a thank you template.

###### `templates` folder

- `admin` folder contains code for `base_site.html` copied from Django's source code. This was done to modify the admin site template to include a link for `Survey Insights`.
- `base.html` is our default layout with HTML boilerplate.
- `error.html` is a simple, customizable error template.
- `home.html` is our homepage template.
- `insights.html` is the template that shows the admin-only `Survey Insights`.
- `quiz.html` contains code for our `QuizView`.
- `thanks.html` is a minimal thank you page.

###### `.env` contains our environment variables

###### `db.sqlite3` is our file-based SQLite3 database

###### `manage.py` is our Django command-line utility

###### `requirements.txt` contains all 3rd party dependencies

### Usage Guidelines:

###### Website Visitor

- Visit the root URL
- Click begin to start the survey
- Answer each question to proceed to the next. All questions are mandatory.
- Enter your email when prompted for
- Check your inbox for the personalized PDF report with your survey score.

###### Website Administrator

- Create relevant and strategic questions and answers from the Django Admin at /admin. `createsuperuser` to create an admin account.
- View `Survey Insights` by clicking on the link at the top-right of the administration site navbar.

### Inspiration:

This project was inspired by the likes of ConvertKit which is a seamless system that allows lead generation, emailing and analytics. This project is a prototype in development.

_Thanks for reading!_
