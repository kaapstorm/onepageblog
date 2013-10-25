# This file is part of onepageblog.
# 
# onepageblog is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# onepageblog is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with onepageblog.  If not, see <http://www.gnu.org/licenses/>.

from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.template.defaultfilters import slugify

from onepageblog.tips.models import Tip


class TipForm(ModelForm):
    """This form is used by site visitors to submit tips
    """
    class Meta:
        model = Tip
        fields = ('title', 'content_markdown')


class UserChangeForm(DjangoUserChangeForm):
    """Simplifies Django's standard UserChangeForm to include only username,
    first_name, last_name and email fields.
    """
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
