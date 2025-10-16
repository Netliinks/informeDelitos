#from django import forms

#class UploadExcelForm(forms.Form):
 #   archivo = forms.FileField(label="Archivo Excel")

#class FiltroRadioForm(forms.Form):
#    radio_km = forms.FloatField(
#        label="Radio en metros",
#        min_value=1,
#        max_value=1000,
#        required=True
#    )
#    delito_dnpj = forms.ChoiceField(
#        label="Filtrar por DELITO DNPJ",
##        required=False,
 #       choices=[],  # Esto se llenará dinámicamente desde la view
 #   )




#from django import forms

#class UploadExcelForm(forms.Form):
#    archivo = forms.FileField()


#class FiltroRadioForm(forms.Form):
    #lat_centro = forms.FloatField(label='Latitud del centro')
    #lon_centro = forms.FloatField(label='Longitud del centro')
    #radio_km = forms.FloatField(label='Radio (metros)')
    #radio_km = forms.FloatField(label="Radio (metros)")

#from django import forms

#class FiltroRadioForm(forms.Form):
#    radio_km = forms.FloatField(
#        label='Radio en metros',
#        min_value=1,
#        max_value=1000,
#        required=True,
#        widget=forms.NumberInput(attrs={'placeholder': 'Ej. 500'})
#    )

#    delito_dnpj = forms.ChoiceField(
#        label='Filtrar por DELITO DNPJ',
#        required=False,
#        choices=[],  # lo llenaremos dinámicamente en la view
#    )








from django import forms

class FiltroRadioForm(forms.Form):
    radio_km = forms.IntegerField(
        label='Radio en metros', min_value=1, max_value=1000,
        required=False,
        initial=1000
    )

    delito_dnpj = forms.ChoiceField(
        label='Filtrar por DELITO DNPJ',
        required=False
    )

    mes = forms.ChoiceField(
        label='Filtrar por Mes',
        required=False
    )

    def __init__(self, *args, **kwargs):
        delitos_choices = kwargs.pop('delitos_choices', [])
        meses_choices = kwargs.pop('meses_choices', [])
        super().__init__(*args, **kwargs)

        self.fields['delito_dnpj'].choices = [('', 'Todos')] + delitos_choices
        self.fields['mes'].choices = [('', 'Todos')] + meses_choices



#class FiltroRadioForm(forms.Form):
#    radio_km = forms.FloatField(
#        label='Radio (m)',
#        min_value=0.1,
#        max_value=1000,
#        error_messages={
#            'min_value': 'El radio debe ser mayor que 0.',
#            'max_value': 'El radio no debe ser mayor a 1000 km.',
#            'required': 'Este campo es obligatorio.',
#            'invalid': 'Ingresa un número válido.'
#        }
#   )
#   subtipo_delito = forms.ChoiceField(
#        label="Subtipo de delito",
#        required=False
#    )

#    def __init__(self, *args, **kwargs):
#        subtipos = kwargs.pop('subtipos', [])
#        super().__init__(*args, **kwargs)
#        if subtipos:
#            opciones = [(s, s) for s in subtipos]
#            self.fields['subtipo_delito'].choices = [("", "Todos")] + opciones




