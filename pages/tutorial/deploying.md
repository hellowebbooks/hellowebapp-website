# Deploying Your Web App

It's really important for you to know how to push your web app onto the internet
so anyone in the world can access it - unfortunately, this is also one of the
most difficult parts of web app development. I'm going to walk you through the
steps in order to launch your website on Heroku, which is the easiest-to-use
hosting solution, but the steps here are still going to be slightly complicated.
Stick with it, it'll be worth it. If you get stuck, head to the Hello Web App
discussion forum for help:
[http://discuss.hellowebapp.com](http://discuss.hellowebapp.com)

In order to use Heroku, we'll need to install some extra utilities and set up
some extra files. After everything is set up, you can continue to develop
locally and deploy new versions of your web app live with ease.

***Note:** On Windows and something isn't working? Check out the discussion
forums mentioned above for troubleshooting since Windows and Heroku sometimes
don't play nicely together.*

# Setting up Heroku

You'll first need to create a free account with Heroku
([http://hellowebapp.com/32](http://hellowebapp.com/32)), and eventually end up
at your dashboard:

![](images/heroku-dashboard.png) 

Click on the Python button, and Heroku will prompt you to install the Heroku
Toolbelt  ([http://hellowebapp.com/33](http://hellowebapp.com/33)), which lets
you log in to Heroku and run other Heroku commands from your command line. The
next page of instructions will instruct you to clone an existing project to
learn deployment - ignore these and just move on below. 

### Setting up a public key

If you try to log in to Heroku from your command line and get the error,
`Permission denied (publickey).` we'll need to set up your public/private key.
This is a security measure to uniquely identify you as the developer of this web
app, so Heroku can make sure only you are the one pushing code changes. 

If you already have a public/private key pair set up, feel free to move onto the
next section.

In your command line, generate the public key by running this command:

{linenos=off}
```
$ ssh-keygen -t rsa
```

The default file location in which to save the key is fine, just press enter at
the prompt. Second, it'll ask for a passphrase - choose something secure that
you'll remember. The final output should look something like this:

{linenos=off}
```
$ ssh-keygen -t rsa
Generating public/private rsa key pair.
Enter file in which to save the key (/Users/limedaring/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /Users/limedaring/.ssh/id_rsa.
Your public key has been saved in /Users/limedaring/.ssh/id_rsa.pub.
The key fingerprint is:
a6:88:0a:0b:74:90:c6:e9:d5:49:d6:e3:04:d5:6c:3e limedaring@workstation.local
```

Once you log in again using `heroku login` in your command line, Heroku should
find and upload your private key automatically.

## Installing a few extra packages

We'll need to install a few other packages required by Heroku. Make sure you're
in your virtual environment, then run `pip install hellowebapp-deploy` in your
command line. This will install:

* *waitress*: A web server for Python apps.
* *dj-database-url*: A Django configuration helper.
* *whitenoise*: Allows you to serve static files in production.

In the previous chapter, we created a *requirements.txt* file. Now that we've
installed new packages, make sure to update it. Rather than piping `pip freeze`
over, we're just going to open up and add `hellowebapp-deploy` to the list like
below:

{title="requirements.txt", lang="python”}
```
Django==1.9.1
django-registration-redux==1.3
wsgiref==0.1.2
# leanpub-start-insert
hellowebapp-deploy
# leanpub-end-insert
```

We're not adding a version number, so pip will install the latest version when
we install our requirements. Also, why not `pip freeze > requirements.txt`? Run
`pip freeze` in your command line, and you should see something like below:

{linenos=off}
```
$ pip freeze
Django==1.9.1
dj-database-url==0.3.0
django-registration-redux==1.3
waitress==0.8.10
hellowebapp-deploy==1.0.2
whitenoise==2.0.6
wsgiref==0.1.2
```

`hellowebapp-deploy` installs the rest of those packages, no need to clutter up
our *requirements.txt* file with the extra installs.

There's one last thing we're going to add to our *requirements.txt* file, that
we're *not* going to install - `psycopg2`. Heroku's database will be
*PostgreSQL* (more on this below), and Heroku will be using our
*requirements.txt* to know what to install on our server. `psycopg2` is a
PostgreSQL adapter for Python, required by Heroku. Locally though, we're using
SQLite3 for our database, because it's 100x easier to set up than PostgreSQL for
beginners. If we installed `psycopg2` locally, it would throw an error because
PostgreSQL isn't installed on your system. So we're going to add it to our
*requirements.txt* so Heroku installs it, but not install it locally.

{title="requirements.txt”, lang="python”}
```
Django==1.8.4
django-registration-redux==1.3
wsgiref==0.1.2
hellowebapp-deploy
# leanpub-start-insert
psycopg2==2.6.1
# leanpub-end-insert
```

## Creating your Procfile

A "Procfile" is something Heroku defined to let users run all kinds of different
applications on their platform. Way back when, you could only run Ruby
applications on Heroku, but thanks to the Procfile you can run your Django
application there too (More info:
[http://hellowebapp.com/34](http://hellowebapp.com/34)).

Let's make a Procfile in our top level directory (the one with *manage.py*) to
tell Heroku how to run our app: 

{linenos=off}
```
$ touch Procfile
```

And update it to the below:

{title="Procfile”, lang="text”}
```
web: waitress-serve --port=$PORT hellowebapp.wsgi:application
```

This tells Heroku that we want to run a process under the "web" category using
waitress, the Python web server we installed earlier.

## Setting up your static files for production

Django serves your static files up in a working, but inefficient manner when
you're developing on your computer. Because of its inefficiency and likely
vulnerabilities, we need to take a couple of different steps to get static files
working in production on our live website. One of the packages we installed
through `hellowebapp-deploy`, `whitenoise`, will help us out here. We just need
to configure a few things.

Update the `wsgi.py` file that was automatically created when we made our Django
project way back in the day to the below:

{title="wsgi.py”, lang="python”, line-numbers=on,starting-line-number=10}
```
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
    "hellowebapp.settings")

from django.core.wsgi import get_wsgi_application
# leanpub-start-insert
from whitenoise.django import DjangoWhiteNoise
# leanpub-end-insert

application = get_wsgi_application()
# leanpub-start-insert
application = DjangoWhiteNoise(application)
# leanpub-end-insert
```

We then need to update *settings.py* for DjangoWhiteNoise. Add `STATIC_ROOT =
'staticfiles'` below `STATIC_URL`:

{title="settings.py”, lang="python”, line-numbers=on,starting-line-number=84}
```
STATIC_URL = '/static/'
# leanpub-start-insert
STATIC_ROOT = 'staticfiles'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
# leanpub-end-insert
```

There's one last silly thing we need to do to set up static files on Heroku.
Heroku will automatically run the command `collectstatic` on your app, which
collect *all* static files into one folder. However, this process will fail if
we don't give it an empty folder to store these files in.

In the same directory as `manage.py`, create a new `static` directory and add an
empty file to it:

{linenos=off}
```
$ mkdir static
$ cd static
static $ touch robots.txt
```

(I'm adding *robots.txt* just because you might need it later on, and it's fine
being blank for now.)

## Creating your app on Heroku

Let's tell Heroku this is the project we want to deploy. Run this in your
command line:

{linenos=off}
```
$ heroku create
```

This will create a "space" for your app in your Heroku account.

Heroku uses git to push our code, so make sure everything is committed at this
point:

{linenos=off}
```
$ git commit -a -m "Committing before pushing to Heroku."
```

Let's push our code to Heroku, which you can do by running this command:

{linenos=off}
```
$ git push heroku master
```

You're going to see a lot of processes fly by — Heroku installing the packages
you've installed like Django and hellowebapp-deploy, moving over your static
files, and starting the server. 

Last, add a web process to your app, which Heroku calls "dynos." Basically, this
tells Heroku to actually start serving your website:

{linenos=off}
```
$ heroku ps:scale web=1
```

We're not quite ready to launch the website — the last thing we need to do is
set up our database.

## Setting up your production database

Way back in the day when we created our local database, we made a SQLite
database, which is the easiest to create, but not good for production on your
live server.

***Reminder**: SQLite3 databases are perfect for small single-user applications,
like ones that run on your computer and only you're using them. Web browsers
such as Safari use SQLite to store and query all kinds of data. They're not
stable when many people try to use your application at once, like when it's
served on the public Internet.*

We're going to set up a separate settings file that'll be used only in Heroku.
That way we can use a production-ready database (As mentioned above,
PostgreSQL). This is also useful if you ever work with something that has "test"
and "live" API keys, so you can put your test API key in your local settings
file and put your live key in your production settings file (for example,
working with Stripe for payments).

In the same folder as *settings.py*, create *settings_production.py*:

{linenos=off}
```
$ cd hellowebapp
hellowebapp $ touch settings_production.py
```

And insert the following information:

{title="settings_production.py”, lang="python”}
```
# Inherit from standard settings file for defaults
from hellowebapp.settings import *

# Everything below will override our standard settings:

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Set debug to False
DEBUG = False 

# Static asset configuration
STATICFILES_STORAGE = \
    'whitenoise.django.GzipManifestStaticFilesStorage'
```

We're basically copy and pasting directly from Heroku's documentation on how to
create a PostgreSQL database (More info:
[http://hellowebapp.com/35](http://hellowebapp.com/35)).

We also need to tell Heroku to use this settings file instead. Paste this into
your command line (make sure you're in the same folder as *manage.py*):

{linenos=off}
```
$ heroku config:set DJANGO_SETTINGS_MODULE=hellowebapp.settings_production
```

As well as update your *wsgi.py* file:

{title="wsgi.py”, lang="python”, line-numbers=on,starting-line-number=11}
```
# leanpub-start-insert
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
    "hellowebapp.settings_production")
# leanpub-end-insert
```

Add the file to git, commit, and push your changes to Heroku:

{linenos=off}
```
$ git add .
$ git commit -a -m "Added production settings file."
$ git push heroku master
```

### Run your migrations on your production server

Here's where you'll start to see why we do database migrations — we can easily
apply all the changes we made locally by running migrate on the server:

{linenos=off}
```
$ heroku run python manage.py migrate
```

Last, we need to create a superuser again on the live server, like we did for
our local server:

{linenos=off}
```
$ heroku run python manage.py createsuperuser
```

Your app should be ready! Run `heroku open` to pop it open in your browser.

Feel free to give your Heroku app a new name (rather than the random one Heroku
gives you) by running the below command (replace `YOURAPPNAME` with a unique
name for your app.)

{linenos=off}
```
$ heroku apps:rename YOURAPPNAME
```

Congrats, you've launched your web app!

For the future, as you develop locally, run the below steps to push it live:

* Commit your changes to git when you're ready to deploy.
* Run `git push heroku master` to push the changes to Heroku.
* Also worth it to run `git push origin master` if you've set up a remote GitHub
    repository to back your app up in the cloud. 
