import os
import random
import time
import webbrowser
from datetime import datetime
from playsound import playsound
import speech_recognition as sr
from gtts import gTTS
import pyaudio
import googlemaps
import smtplib
import ssl
from email.message import EmailMessage


nasilsin = ["nasılsın", "naber", "ne haber", "napıyorsun",
           "nasıl gidiyor", "naber", "napıyon", "nasıl", "nabıyon"]
donus = ["iyiyim sen", "çok iyiyim", "biraz keyifsizim"]
notal = ["not al", "not alır mısın", "not tut", "not"]
notoku = ["notlarımı oku", "notları oku", "notlar","not oku"]
video = ["video aç","müzik aç","youtube aç"]


class SesliAsistan():
    def speak(self,metin):
        destiny=gTTS(text=metin, lang="tr")
        dosya="dosya"+str(random.randint(0, 32543687586986775674))+".mp3"
        destiny.save(dosya) #oluşturulan ses mp3 olarak kaydedildi
        playsound(dosya)  # oluşturulan dosya okundu
        os.remove(dosya) #oluşturulan ses dosyası silindi
        print(metin)

    def record(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            print("Seni dinliyorum...")
            audio=r.listen(source)
            voice=" "
            try:
                voice=r.recognize_google(audio, language="tr-TR")
                time.sleep(1)
                print(voice)
            except sr.UnknownValueError:
                self.speak("Sesin anlaşılır değil tekrar söylermisin")
            return voice

    def welcome(self):
        self.saat = datetime.now().hour
        if self.saat >= 0 and self.saat < 12:
            self.speak("Günaydın")
        elif self.saat >= 12 and self.saat < 19:
            self.speak("İyi Günler")
        else:
            self.speak("İyi Akşamlar")
        self.speak("Hoşgeldin ben luna nasıl yardımcı olabilirim")

    def mail (self,receiver,mesaj,subject):
        sender="Your mail"
        password="Your password"
        msg=EmailMessage()
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = receiver
        msg.set_content(mesaj)
        context = ssl.create_default_context()
        with smtplib.SMTP("SMTP.office365.com",587) as server:
            server.starttls(context=context)
            server.login(sender,password)
            server.send_message(msg)

    def answer(self, audio):
        if "luna" in audio:
            self.speak("Sana nasıl yardımcı olabilirim")
        elif "selam" in audio:
            self.speak("Aleykümselam nasılsın bakalım")
        elif audio in nasilsin:
            self.speak(donus[random.randint(0,2)])
        elif "arama yap" in audio:
            self.speak("Ne aramak istiyorsun")
            urlara="https://www.google.com/search?q="+ format(self.record())
            webbrowser.get().open_new(urlara)
        elif "saat kaç" in audio:
            self.speak(datetime.now().strftime('%H:%M:%S'))
        elif audio in video:
            self.speak("ne açmamı istiyorsun")
            veri=self.record()
            self.speak("{} açılıyor..".format(veri))
            url = "https://www.youtube.com/results?search_query={}".format(veri)
            time.sleep(1)
            browser = webbrowser.get().open_new(url)
        elif audio in notal:
            self.speak("not alıyorum")
            file = open("notlar.txt", "w")
            audio = self.record()
            file.write(str(audio))
            file.close()
            self.speak("not aldım")
        elif audio in notoku:
            file=open("notlar.txt", "r")
            self.speak("alınan notlar")
            self.speak(file.read())
            self.speak("alınan notlar bu kadar")
            time.sleep(1)
        elif "mail gönder" in audio:
            self.speak("Alıcı e mail lütfen")
            receiver = "Receiver mail"
            print(receiver)
            self.speak("Konu başlığı: ")
            subject = self.record()
            self.speak("Göndermek istediğiniz mesaj : ")
            mesaj = self.record()
            self.mail(receiver, mesaj, subject)
            self.speak("Mail gönderildi!!!")
            print(self.speak)
        elif "adres bul" in audio:
            self.speak("Gidilecek lokasyon: ")
            location = self.record()
            url = 'https://google.com.tr/maps/search/' + location + '/&amp;'
            webbrowser.get().open(url)
            print("Konum bulunuyor...")
            self.speak("Konum Bulundu:" + location)
        elif "konum bul" in audio:
            self.speak("Başlangıç konumu")
            baslangic = self.record()
            self.speak("Gidilecek konum")
            gidis = self.record()
            print("Konum bulunuyor...")
            api_file = open("api_key.txt", "r")
            api_key = api_file.read()
            api_file.close()
            gmaps = googlemaps.Client(api_key)
            now = datetime.now()
            directions_result = gmaps.directions(baslangic, gidis, mode="driving",departure_time=now,language="tr-TR")
            self.speak("Konum Bulundu:")
            mesafe=directions_result[0]['legs'][0]['distance']['text']
            print("Gidilecek mesafe : "+mesafe)
            self.speak(baslangic+" ve "+gidis+" arasındaki mesafe "+mesafe)
            gidis_suresi=directions_result[0]['legs'][0]['duration']['text']
            print("Gidiş süresi : "+gidis_suresi)
            self.speak("Gidiş süresi "+gidis_suresi)
            url = 'https://www.google.com/maps/dir/' + baslangic + '/' + gidis
            webbrowser.get().open(url)


asistan=SesliAsistan()
asistan.welcome()
while True:
    ses=asistan.record()
    if(ses!=" "):
        ses=ses.lower()
        asistan.answer(ses)
        print(ses)



