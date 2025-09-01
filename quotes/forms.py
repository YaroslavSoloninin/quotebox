from django import forms
from .models import Quote, Source


class QuoteForm(forms.ModelForm):
    book = forms.ModelChoiceField(
        queryset=Source.objects.filter(type='book'),
        empty_label="Выберите книгу",
        required=False,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    movie = forms.ModelChoiceField(
        queryset=Source.objects.filter(type='movie'),
        empty_label="Выберите фильм",
        required=False,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = Quote
        fields = ["text", "book", "movie", "weight"]
        labels = {
            "text": "",
            "weight": "",
        }
        widgets = {
            "text": forms.Textarea(attrs={
                "rows": 3,
                "class": "form-control",
                "placeholder": "Введите цитату",
                "style": "max-height: 200px;"
            }),
            "weight": forms.Select(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        book = cleaned_data.get("book")
        movie = cleaned_data.get("movie")

        if not book and not movie:
            raise forms.ValidationError("Выберите книгу или фильм")
        if book and movie:
            raise forms.ValidationError("Нельзя выбирать одновременно и книгу и фильм")
        if (book and book.quotes.count() >= 3) or (movie and movie.quotes.count() >= 3):
            raise forms.ValidationError(f"У одного источника не может быть больше трех цитат")

        self.cleaned_data['source'] = book if book else movie
        return cleaned_data


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ('name', 'type')
        labels = {
            'name': '', 'type': ''
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Название"}),
            "type": forms.Select(attrs={"class": "form-control"}),
        }
