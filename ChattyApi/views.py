from django.shortcuts import render
import nltk
from spellchecker import SpellChecker
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
class CorrectText(APIView):
    def get(self, request):
        print(request)
        tokenizer = nltk.tokenize.WhitespaceTokenizer()
        tokens = tokenizer.tokenize(request.data["text"])
        spell = SpellChecker()
        words = [] 
        for word in tokens:
            if (word.istitle()):
                words.append(word)
            else :
                words.append(spell.correction(word))
        print(" ".join(words))
        return Response({"text": " ".join(words)})


