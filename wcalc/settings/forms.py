from django import forms

from .models import SettingsPortal


class SettingsPortalForm(forms.ModelForm):
    """Форма Настройки портала."""

    class Meta:
        model = SettingsPortal
        fields = ('quantity_pallet_code', 'tonnage_code')
