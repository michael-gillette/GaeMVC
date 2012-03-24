#sb_referrals/forms.py
def validate_multi_emails(value):
	values  = value.split('\n')
	unique  = set(values)
	
	# make sure at least 5 unique emails entered
	if len(unique) < 5:
		raise ValidationError(_("Enter at least 5 emails"))
	
	# make sure these are indeed emails
	if not all(email_re.match(email) for email in unique):
		raise ValidationError(_("Double check all email address"))
	
	# check database for discounts related to emails
	existing_discounts = DiscountReferral.objects.filter(email__in=emails)
	
	if existing_discounts.count():
		raise ValidationError(_("Some email addresses are in use: ") + ", ".join(unique))

class ReferralForm( forms.Form ):
	referrer  = forms.CharField(max_length=100)
	referrals = forms.CharField(widget=forms.widgets.Textarea(attrs={ 'rows': 5, 'cols': 30 }),validators=[validate_multi_emails])