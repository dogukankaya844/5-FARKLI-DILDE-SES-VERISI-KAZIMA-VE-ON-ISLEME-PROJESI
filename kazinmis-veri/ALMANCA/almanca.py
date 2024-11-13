from googleapiclient.discovery import build 
import yt_dlp
import os

# YouTube API anahtarınızı buraya girin
api_anahtari = "AIzaSyCXBVkURd1n57bG6b7WpTZfe8jBpivlBlM"

# YouTube API'sine bağlanın
youtube = build('youtube', 'v3', developerKey=api_anahtari)


# Playlist ID'yi direkt olarak oynatma listesi URL'sinden alıyoruz
calma_listesi_id = "PLslDofkqdKI-P-CkoBH-YBxBj8sqPHKHs"

# Yükleme listesinde bulunan videoları al
def calma_listesinden_videolari_al(calma_listesi_id, maksimum_sonuc=5000):
    video_url_listesi = [] #Videoların URL'lerini saklamak için boş bir liste oluşturuyoruz.
    sonraki_sayfa_token = None #API'den gelecek olan sonraki sayfa bilgisi için bir değişken tanımlıyoruz. 
    while len(video_url_listesi) < maksimum_sonuc:
        try:
            istek = youtube.playlistItems().list( #YouTube API'sine çalma listesindeki videoları almak için bir istek oluşturuyoruz.
                part="snippet", #API'den hangi tür bilgileri almak istediğimizi belirtiyoruz. Burada "snippet", videonun temel bilgilerini ifade eder.
                playlistId=calma_listesi_id, #Daha önce belirlediğimiz çalma listesinin kimliğini buraya koyuyoruz.
                maxResults=50,  # YouTube API'sinin limitini aşmamak için 50 ile sınırlandırıyoruz
                pageToken=sonraki_sayfa_token #Eğer daha önce başka bir sayfadan veriler aldıysak, sonraki sayfayı almak için bu değişkeni kullanıyoruz.
            )
            yanit = istek.execute() #API isteğini çalıştırıyor ve yanıtı alıyoruz.

            if 'items' not in yanit or len(yanit['items']) == 0: 
                print("Daha fazla video bulunamadı.")   #Eğer yanıt içinde 'items' anahtarı yoksa veya uzunluğu 0 ise (yani video yoksa) mesaj yazdırıyoruz ve döngüyü kırıyoruz.
                break

            for oge in yanit['items']: #Yanıtın içindeki her bir video öğesi için döngü başlatıyoruz.
                video_url_listesi.append(f"https://www.youtube.com/watch?v={oge['snippet']['resourceId']['videoId']}") #Her bir video için URL'yi oluşturup video_urls listesine ekliyoruz. URL, videoId kullanılarak oluşturuluyor.
                
                # Maksimum sayıya ulaştıysak döngüyü kır
                if len(video_url_listesi) >= maksimum_sonuc:
                    break

            # Bir sonraki sayfa token'ını al
            sonraki_sayfa_token = yanit.get('nextPageToken')#Eğer daha fazla sayfa varsa, sonraki sayfa token'ını alıyoruz bir sonraki istekte kullanmak için.

            # Eğer başka sayfa yoksa döngüyü kır
            if not sonraki_sayfa_token:
                break
        except Exception as hata:
            print(f"Calma listesinden videolar alinirken hata olustu: {hata}")#Eğer bir hata meydana gelirse, hatayı yakalayıp bir mesaj yazdırıyoruz ve döngüyü kırıyoruz.
            break

    return video_url_listesi #Fonksiyon, topladığımız video URL'lerini içeren listeyi döndürüyor.

def videoyu_mp3_olarak_indir(video_url, cikti_dizini):
    # İndirme seçenekleri
    ydl_secenekleri = {
        'format': 'bestaudio/best',  # En iyi ses kalitesini indir
        'outtmpl': f'{cikti_dizini}/%(title)s.%(ext)s',  # Çıktı dosya yolu #İndirilen dosyanın kaydedileceği yol ve dosya adı şablonu. 
        #Burada, çıktı_dizini içinde dosya adı olarak video başlığı kullanılacak.
        'postprocessors': [{#İndirme sonrası işleme ayarları. Burada, ses dosyasını MP3 formatına dönüştürmek için FFmpeg kullanılıyor.
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3', #format mp3
            'preferredquality': '192', #dosya kalitesi 192kbps
        }],
        'postprocessor_args': [#Dönüştürme sırasında kullanılacak ek argümanlar.
            '-t', '60'  # Sadece ilk 60 saniyeyi kes
        ],
        'quiet': True  #İndirme işlemi sırasında çok fazla çıktı vermemesi için sessiz mod.
    }

    try:
        with yt_dlp.YoutubeDL(ydl_secenekleri) as ydl: #yt_dlp kütüphanesinin YoutubeDL sınıfından bir nesne oluşturuluyor ve ydl olarak adlandırılıyor. 
        #Bu nesne, daha önce belirlenen ydl_seçenekleri ile çalışacak.
            bilgi_dict = ydl.extract_info(video_url, download=False)#Video URL'sinden bilgi almak için extract_info metodu kullanılıyor. 
        #download=False parametresi ile sadece bilgi alınıyor; video indirilmez.
            sure = bilgi_dict.get('duration', 0)#Alınan bilgi sözlüğünden video süresi alınıyor. 
        #Eğer süre bulunamazsa, varsayılan değer 0 olarak atanıyor.
            video_basligi = bilgi_dict['title']#Videonun başlığı alınıyor.

        # Eğer video 60 saniye veya daha uzunsa, sadece ilk 1 dakikasını indir
        if sure >= 60:
            print(f"Videonun ilk 1 dakikasını indiriyorum ve dönüştürüyorum: {video_basligi}")
            ydl.download([video_url])#Video URL'si kullanılarak video indirme işlemi başlatılıyor.
        else:
            print(f"Video 1 dakikadan kısa olduğu için atlanıyor: {video_basligi}")#Kullanıcıya, videonun kısa olduğu ve indirilmediği bilgisi veriliyor.

    except Exception as hata:
        print(f"Hata: {hata}")#Eğer yukarıdaki kod bloklarında bir hata meydana gelirse, hata yakalanıyor
    #Hatanın detayları kullanıcıya yazdırılıyor.

# Çalma listesinde videoları al
almanca_videolar = calma_listesinden_videolari_al(calma_listesi_id, maksimum_sonuc=5000) #playlist'teki videolar alınır. 
#playlist_id ve max_results parametreleri kullanılarak istenilen video sayısı alınır.

# Çıktı dizini
cikti_dizini = "C:\\Users\\Niyazi\\Desktop\\kazinmis-veri\\ALMANCA\\almanca-ham"  # Çıktı dizinini buraya yazın

# Her bir videoyu indir ve 1 dakikalık MP3 olarak kaydet
for video in almanca_videolar: #german_videos listesindeki her bir video için döngü başlatılıyor.
    videoyu_mp3_olarak_indir(video, cikti_dizini) #Her bir video URL'si kullanılarak fonksiyon çağrılıyor ve video MP3 formatında belirtilen dizine kaydediliyor.
    