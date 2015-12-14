from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from .forms import SignUpForm, ContactForm
from .models import SignUp

def home(request):
    title = "Join Us Now!"
    form = SignUpForm(request.POST or None)

    context = {
        "title": title,
        "form": form,
    }

    if form.is_valid():
        instance = form.save(commit=False)
        if not instance.full_name:
            instance.full_name = "Visitor"
        instance.save()

        context = {
            "title": "Thank you!"
        }

    if request.user.is_authenticated() and request.user.is_staff:
        # print SignUp.objects.all()
        # for instance in SignUp.objects.all():
        #     print instance.full_name
        queryset = SignUp.objects.all().order_by("-timestamp")
        print SignUp.objects.all().order_by("-timestamp").filter(full_name__icontains="Alex").count()
        context = {
            "queryset": queryset,
        }

    return render(request, "home.html", context)


def contact(request):
    title = "Contact Us"
    title_align_center = True
    form = ContactForm(request.POST or None)
    if form.is_valid():
        # for key, value in form.cleaned_data.iteritems():
        #     print key, value
        #     #print form.cleaned_data.get(key)
        form_email = form.cleaned_data.get("email")
        form_message  = form.cleaned_data.get("message")
        form_full_name = form.cleaned_data.get("full_name")
        # print email, message, full_name
        subject = 'Site contact form'
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email]
        contact_message = "%s: %s via %s" % (form_full_name, form_message, form_email)
        html_message = "<h1>Hello</h1>"
        send_mail(subject,
                  contact_message,
                  from_email,
                  to_email,
                  html_message=html_message,
                  fail_silently=False)
    context = {
        "form": form,
        "title": title,
        "title_align_center": title_align_center,
    }

    return render(request, "forms.html", context)
