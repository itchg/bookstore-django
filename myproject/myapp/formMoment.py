from django.forms import ModelForm
from myapp.models import Moment

class MomentForm(ModelForm):
    class Meta:
        model = Moment
        fields = '__all__'