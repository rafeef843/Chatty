from django.shortcuts import render
import nltk
from spellchecker import SpellChecker
from rest_framework.response import Response
from rest_framework.views import APIView
from urllib.request import *
from autocorrect import Speller
# Create your views here.
class CorrectText(APIView):
    def spellChecker (self , text ):
        tokenizer = nltk.tokenize.WhitespaceTokenizer()
        tokens = tokenizer.tokenize(text)
        spell = SpellChecker()
        words = [] 
        for word in tokens:
            if (word.istitle()):
                words.append(word)
            else :
                words.append(spell.correction(word))
        return  " ".join(words)
    
    def autoCorrect(self , text ):
        spell = Speller()
        return spell(text)

    def get(self, request):
        text = request.data["text"]
        #res = self.spellChecker(text)
        res = self.autoCorrect(text)
        return Response({"text": res })


class Action(APIView):
    def getSolrResponse(self,text):
        connection = urlopen('http://localhost:8983/solr/sql_test_core/select?q='+text)
        response = eval(connection.read())
        res = response["response"]
        return res
    def get(self, request):
        text = request.data["text"]
        q1 = text.strip().replace(" " , "*%20OR%20") 
        res1 = self.getSolrResponse("CommandString%3A(" + q1 + ")")
        if len(res1['docs']) > 0 : 
            text = text.replace(res1["docs"][0]['CommandString'][0] , "").strip()
            if text.startswith("to"):
                text = text[3:]
            q2 = text.strip().replace(" " , "*%20OR%20") 
            presons_res = self.getSolrResponse("personField%3A(" + q2 + ")")
            if len(presons_res['docs']) > 0 :
                email = presons_res['docs'][0]["PersonEmail"][0]
                nameAr = presons_res['docs'][0]["PersonNameAr"][0]
                nameEn = presons_res['docs'][0]["PersonNameEn"][0]
                text = text.replace(presons_res["docs"][0]['PersonEmail'][0] , "").strip()
                text = text.replace(presons_res["docs"][0]['PersonNameAr'][0] , "").strip()
                text = text.replace(presons_res["docs"][0]['PersonNameEn'][0].lower() , "").strip()
                action_response =  {
                    "ActionName": "Send Email" ,
                    "toEmail" : email ,
                    "toArabicName" : nameAr,
                    "toEnglishName" : nameEn , 
                    "Subject" : text 
                }
                return Response({"Action":action_response})
        return Response({"Error": "Action Not FOUND"})

