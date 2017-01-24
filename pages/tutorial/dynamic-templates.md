# Displaying Dynamic Information in the Templates

It's great that we can see our information in the admin, but now we need to be
able to display that information in our templates and ergo in our website.

## Querying for info from the database

Views are where all of our logic will go for displaying in the templates, so
it's back to *views.py* we go.

Find the index view back from when we were playing with template tags:

{title="views.py", lang="python", line-numbers=on, starting-line-number=4}
```
def index(request):
    number = 6
    # don't forget the quotes since it's a string, 
    # not an integer
    thing = "Thing name" 
    return render(request, ‘index.html', {
        'number': number,
        # don't forget to pass it in, and the last comma
        'thing': thing,
    })
```

Right now it's essentially saying: "When the index page is viewed, display this
template and pass along these two variables." 

Now we want to update that to, "When the index page is viewed, find all things
in our database, display this template, and pass those things along to that
template." 

Here's the new view. Don't forget, if you've renamed `Thing` to something else
in your model, make sure to update all instances below:

{title="views.py", lang="python"}
```
from django.shortcuts import render
# leanpub-start-insert
from collection.models import Thing
# leanpub-end-insert

# the rewritten view!
def index(request):
    # leanpub-start-insert
    things = Thing.objects.all()
    # leanpub-end-insert
    return render(request, ‘index.html', {
    # leanpub-start-insert
        'things': things,
    # leanpub-end-insert
    })
```

First, we need to tell the view that we need some information from the model, so
we've added an import statement to the top of the page (that's the `from
collection.models import Thing`).

Then in the index view, we're using QuerySets (More info:
[http://hellowebapp.com/18](http://hellowebapp.com/18)) to ask for all `Thing`
objects from the database. 

Head back to the template, where we were having fun with template tags before.
We now are passing along a variable containing all the `Thing`s in our database,
so now we need to display that in the template.

Update your *index.html*:

{title="index.html", lang="html+django"}
```
{% extends 'base.html' %}
{% block title %}
    Homepage - {{ block.super }}
{% endblock title %}

{% block content %}
    # leanpub-start-insert
    {% for thing in things %}
    <h2>{{ thing.name }}</h2>
    <p>{{ thing.description }}</p>
    {% endfor %}
    # leanpub-end-insert
{% endblock content %}
```

This is a loop that'll iterate over all the objects in the `things` variable,
displaying the name for each `Thing`. Remember that `{% %}` shows an action and
`{{ }}` prints out the variable.

Voilà: We're showing the information from our database in our homepage!

![](images/things_added_homepage.png) 

## Retrieving and filtering information with QuerySets

One of the biggest things to remember about programming is that accessing the
database is one of the slowest things your app can do, and can lead to a slow
website if you're not careful. That means querying for all `Thing`s when you
only want one `Thing` is inefficient. *Don't* do something like this in your
template:

{linenos=off}
```
{% for thing in things %}
    {% if thing.name == "Hello" %}
        {{ thing.name }}
    {% endif %}
{% endfor %}
```

It would be much faster if we could just query for that one `Thing` instead,
rather than getting all of them and then just searching for just one in the
template, right?

QuerySets come with a lot of extra stuff to help filter the records in your
database. For example, if you wanted the `Thing` named "Hello," you could do
this instead:

{linenos=off}
```
# what we had before
things = Thing.objects.all()

# just getting one object!
correct_thing = Thing.objects.get(name='Hello')
```

The `.get()` method will retrieve the object that matches the query, but keep in
mind it'll throw an error if more than one object is found (or none.) If you
want to grab a bunch of things that match, you'll use `.filter()`:

{linenos=off}
```
things = Thing.objects.filter(name='Hello')
```

So, remember: `.get()` is when you want one, exact object; `.filter()` is for
when you could possibly retrieve more than one result.

When Django returns a bunch of items, we can also have it return it
alphabetically using `.order_by()`:

{linenos=off}
```
things = Thing.objects.filter(name='Hello').order_by('name')
```

Another useful method is to look up whether a field contains something using
`contains`:

{linenos=off}
```
things = Thing.objects.filter(name__contains='Hello')
```

Check out your website to see the update:

![](images/things_order.png) 

Note how `contains` gets added onto the field that we're searching on using a
double-underscore (`__`). If we had just `name=`, we'd only get **exact** name
matches, but `name__contains=` will get **incomplete** matches.

We can also tell it to return a random order as well using `?`:

{linenos=off}
```
things = Thing.objects.all().order_by('?')
```

This is just an overview of the basic queries we can make with Django. For more
(a lot more, but it's pretty interesting), check out Django's documentation of
QuerySets: [http://hellowebapp.com/18](http://hellowebapp.com/18).

Before you forget, change the query in your view back to grabbing all objects:

{title="views.py", lang="python"}
```
from django.shortcuts import render

from collection.models import Thing

def index(request):
    # leanpub-start-insert
    things = Thing.objects.all()
    # leanpub-end-insert
    return render(request, ‘index.html', {
        'things': things,
    })
```

Congrats — we now have objects in our database showing up on our website! Commit
your work, and now let's move on to creating individual pages for these objects.
