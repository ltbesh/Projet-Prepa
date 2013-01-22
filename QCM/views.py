from django.template import RequestContext
from django.http import HttpResponse
from QCM.models import Question
from random import randint
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
import datetime, random, sha
from django.shortcuts import render_to_response, get_object_or_404
from django.core.mail import send_mail
from QCM.models import UserProfile
#from QCM.forms import RegistrationForm

@login_required()
def index(request):
	return render_to_response('QCM/index.html',context_instance=RequestContext(request))

@login_required()
def qcm(request):
	questions = Question.objects.filter(subject = 'mathematique')
	number = randint(0,len(questions)-1)
	question = questions[number]
	return render_to_response('QCM/qcm.html', {'question' : question})

def register(request):
	if request.user.is_authenticated():
		# They already have an account; don't let them register again
		return render_to_response('register.html', {'has_account': True})
	manipulator = RegistrationForm()

	if request.POST:
		new_data = request.POST.copy()
		errors = manipulator.get_validation_errors(new_data)
		if not errors:
			# Save the user                                                                                                                                                 
			manipulator.do_html2python(new_data)
			new_user = manipulator.save(new_data)
			
			# Build the activation key for their account                                                                                                                    
			salt = sha.new(str(random.random())).hexdigest()[:5]
			activation_key = sha.new(salt+new_user.username).hexdigest()
			key_expires = datetime.datetime.today() + datetime.timedelta(2)
			
			# Create and save their profile                                                                                                                                 
			new_profile = UserProfile(user=new_user,
									  activation_key=activation_key,
									  key_expires=key_expires)
			new_profile.save()
			
			# Send an email with the confirmation link                                                                                                                      
			email_subject = 'Your new ' + PROJECT_NAME + ' account confirmation'
			email_body = "Hello, %s, and thanks for signing up for an \
			" + PROJECT_NAME + " account!\n\nTo activate your account, click this link within 48 \
			hours:\n\n" + PROJECT_URL + "/accounts/confirm/%s" % (
				new_user.username,
				new_profile.activation_key)
			send_mail(email_subject,
					  email_body,
					  'accounts@example.com',
					  [new_user.email])
			
			return render_to_response('register.html', {'created': True})
	else:
		errors = new_data = {}
	form = forms.FormWrapper(manipulator, new_data, errors)
	return render_to_response('register.html', {'form': form})

def confirm(request, activation_key):
	if request.user.is_authenticated():
		return render_to_response('confirm.html', {'has_account': True})
	user_profile = get_object_or_404(UserProfile,
									 activation_key=activation_key)
	if user_profile.key_expires < datetime.datetime.today():
		return render_to_response('confirm.html', {'expired': True})
	user_account = user_profile.user
	user_account.is_active = True
	user_account.save()
	return render_to_response('confirm.html', {'success': True})