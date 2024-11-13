
# YouTube Playlist to MP3 Downloader

Bu proje, bir YouTube oynatma listesinde bulunan videoların ilk 1 dakikasını indirip MP3 formatında kaydetmeyi sağlar. Videoların başlıkları çıktı dosyalarının isimleri olarak belirlenir.

## Gereksinimler

Bu projeyi çalıştırmak için aşağıdaki Python kütüphanelerine ihtiyaç vardır. `kazinmis-veri-gereklilikler.txt` dosyasını kullanarak kolayca yükleyebilirsiniz:

```bash
pip install -r kazinmis-veri-gereklilikler.txt
```

## API Anahtarı

YouTube API'sine erişmek için `YOUR_YOUTUBE_API_KEY` değişkenine kendi YouTube API anahtarınızı girin.

## Kod Yapısı

### 1. YouTube API ile Playlist'ten Video Listesi Alma

`calma_listesinden_videolari_al` fonksiyonu, belirli bir oynatma listesindeki videoların linklerini alır.

- **Parametreler:**
  - `calma_listesi_id` (str): İlgili oynatma listesinin ID’si.
  - `maksimum_sonuc` (int): En fazla alınacak video sayısı. Varsayılan değer 5000.

- **Döndürülenler:**
  - `video_url_listesi` (list): Video URL’lerinin listesi.

### 2. Videoları MP3 Olarak İndirme ve Kayıt

`videoyu_mp3_olarak_indir` fonksiyonu, videoları indirir ve MP3 formatında kaydeder.

- **Parametreler:**
  - `video_url` (str): İndirilecek video URL’si.
  - `cikti_dizini` (str): İndirilen dosyaların kaydedileceği klasör.

Bu fonksiyon, videonun ilk 1 dakikasını MP3 olarak indirir ve `cikti_dizini` altında saklar.

### Kullanım

Kod örneği:

```python
# Playlist'teki videoları al
calma_listesi_id = "PLslDofkqdKI-P-CkoBH-YBxBj8sqPHKHs"  # Örneğin oynatma listesi ID'si
almanca_videolar = calma_listesinden_videolari_al(calma_listesi_id, maksimum_sonuc=5000)

# Çıktı dizini
cikti_dizini = "C:\\Users\\Niyazi\\Desktop\\kazinmis-veri\\ALMANCA\\almanca-ham"

# Videoları indir ve MP3 formatında kaydet
for video in almanca_videolar:
     videoyu_mp3_olarak_indir(video, cikti_dizini)
```

## Çıktılar

İndirilen MP3 dosyaları, belirtilen `cikti_dizini` dizininde yer alır.