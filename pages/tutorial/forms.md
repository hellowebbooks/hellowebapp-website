# Forms.py Funsies

We now have a basic website that showcases a collection of objects, with
individual pages for each object. However at the moment, if you needed to change
any data for an object (basically, change the name or description), you can only
do that through the admin. Let's start working with Django forms and create
pages on the website that'll allow us to update the information for each object
inside the actual website.

## Update your `urls.py` 

As usual, we'll need to do the typical create-a-url, create-a-view,
create-a-template routine we've been doing. So, head back to over to *urls.py*,
and add the indicated line:

{title="urls.py", lang="python"}
```
urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^about/$', 
        TemplateView.as_view(template_name='about.html'),
        name='about'),
    url(r'^contact/$', 
        TemplateView.as_view(template_name='contact.html'),
        name='contact'),
    url(r'^things/(?P<slug>[-\w]+)/$', views.thing_detail',
        name='thing_detail'),
    # new line we're adding!
    # leanpub-start-insert
    url(r'^things/(?P<slug>[-\w]+)/edit/$', 
        views.edit_thing,
        name='edit_thing'),
    # leanpub-end-insert
    url(r'^admin/', admin.site.urls),
]
```

***Note:** We set up our models so that we're assuming one `User` to one
`Thing`. In that case, we actually don't need to include the slug in the URL, so
our future code could be a bit simpler. But I'm going to show you how to do it
this way, because it's more flexible in case you set you web app up so `User`s
can own multiple `Thing`s.*

## And then add your view...

Go to your *views.py* file to add the new view. Add the below code below your
`thing_detail` view (apologies, it's quite the doozy but the comments should
help):

{title="views.py", lang="python"}
```
# add to top of the file
from django.shortcuts import render,
# leanpub-start-insert
                             redirect
# leanpub-end-insert
# leanpub-start-insert
from collection.forms import ThingForm
# leanpub-end-insert
from collection.models import Thing
```

{title="views.py", lang="python", line-numbers=on, starting-line-number=32}
```
# add below your thing_detail view
# leanpub-start-insert
def edit_thing(request, slug):
    # grab the object
    thing = Thing.objects.get(slug=slug)
    # set the form we're using
    form_class = ThingForm

    # if we're coming to this view from a submitted form
    if request.method == 'POST':
        # grab the data from the submitted form and apply to
        # the form
        form = form_class(data=request.POST, instance=thing)
        if form.is_valid():
            # save the new data
            form.save()
            return redirect('thing_detail', slug=thing.slug)
    # otherwise just create the form
    else:
        form = form_class(instance=thing)

    # and render the template
    return render(request, ‘things/edit_thing.html', {
        'thing': thing,
        'form': form,
    })
# leanpub-end-insert
```

The most complicated view we've added yet! We've added an if-statement, which
allows the view to do two different things depending on whether we're just
displaying the form, or dealing with the new data after the form has been
submitted. Multi-use view!

## Create your `forms.py` file

In the view, we make reference to `ThingForm`, which we haven't created yet.
It's really handy to have all your form information in one place, so we're going
to add a file called *forms.py* into our `collection` app.

{linenos=off}
```
$ cd collection
collection $ touch forms.py
```

Open it up and add the following code:

{title="forms.py", lang="python"}
```
from django.forms import ModelForm

from collection.models import Thing

class ThingForm(ModelForm):
    class Meta:
        model = Thing
        fields = ('name', 'description',)
```

A part of Django's "magic" is the ability to create forms directly from your
model — thus, the *ModelForm* (More info:
[http://hellowebapp.com/20](http://hellowebapp.com/20)). We just need to tell it
which model to base itself on, as well as (optionally) which fields we want it
to include. This way we don't allow updating of the slug in the form because it
should be set automatically from the `Thing` name.

So, plainly speaking: This form is based on the `Thing` model, and allows
updating of its `name` and `description` fields.

Last, the template. Head back into your *things* folder and add a template to
edit your object.

{linenos=off}
```
$ cd collection/templates/things
collection/templates/things $ touch edit_thing.html
```

In the view above, you'll see we're passing in the form. Thankfully, Django has
another useful utility for displaying the form in the template. Here's what
we'll add into our template:

{title="edit_thing.html", lang="html+django"}
```
{% extends 'base.html' %}
{% block title %}
    Edit {{ thing.name }} - {{ block.super }}
{% endblock title %}

{% block content %}
    <h1>Edit "{{ thing.name }}"</h1>
    <form role="form" action="" method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Submit</button>
    </form>
{% endblock content %}
```

A couple of things to note:
* What's that whole `{% csrf_token %}` stuff? Django requires this added to
    every form that submits via POST. Long story short, it's *Cross Site Request
    Forgery* protection (More info:
    [http://hellowebapp.com/21](http://hellowebapp.com/21)) that ships with
    Django. The website will complain if you don't have it because it's a
    security measure.
* Adding `.as_p` to our form variable is optional — it'll render the form fields
    wrapped in `<p>` tags. You can also do `.as_ul` (wrapped in `<li>` tags,
    you'll still need to add the surrounding `<ul>` tag) or as `.as_table`
    (you'll still need to add surrounding `<table>` tags.) Read more about that
    here: [http://hellowebapp.com/22](http://hellowebapp.com/22).

To make it easy to access this page, add a link to this page from our object
view:

{title="thing_detail.html", lang="html+django"}
```
{% extends 'base.html' %}
{% block title %}
     {{ thing.name }} - {{ block.super }}
{% endblock title %}

{% block content %}
    <h1>{{ thing.name }}</h1>
    <p>{{ thing.description }}</p>
    # leanpub-start-insert
    <a href="{% url 'edit_thing' slug=thing.slug %}">Edit me!</a>
    # leanpub-end-insert
    {% endblock content %}
```

Head to the browser to check it out:

![](images/new_edit_link.png) 

![](images/new_edit_page.png) 

Neat, all of the form fields already have the current information for the
object. Thanks, Django! Feel free to edit and save any information here and
it'll automagically update the database, and ergo, all the information on your
website.

Now we can update the information about these objects in our website, but still
can only create new objects from our admin. Commit your work. Next, we'll add a
registration page so customers can create pages of their own.

***Note**: While your slug was created automatically based on the Name when we
added the object, changing the name of the object won't change the slug. For
example, if your name was "This Name" and your slug was `this-name`, and you
updated the name to "Another Name", the slug will continue to be `this-name`.
What's up with that? It's actually quite smart — if this page was on the
Internet with people linking to it, and the slug (ergo the URL) changed, all of
the links would break. Django, by default, keeps the slugs the same as when they
were created to make sure all external links continue to work. You can manually
override this in your admin, however.*
