
# Ses İşleme Projesi

Bu proje, bir klasörde bulunan MP3 ses dosyalarını işleyerek gürültü azaltma, normalizasyon, MFCC, Zero-Crossing Oranı ve Kromatik Özellikler çıkarma gibi işlemler gerçekleştirir. İşlenen ses dosyaları, temizlenmiş ses dosyası, özelliklerin görselleştirilmiş hali ve özelliklerin CSV formatında kaydedilmiş hali olarak belirli klasörlerde saklanır.

## Gereksinimler

Bu projeyi çalıştırmak için aşağıdaki Python kütüphanelerine ihtiyaç vardır. Bu kütüphaneleri yüklemek için `gereklilikler.txt` dosyasını kullanabilirsiniz:

```
os-sys
librosa==0.10.0.post2
numpy==1.23.5
noisereduce==0.3.1
matplotlib==3.6.3
soundfile==0.12.1
```

Kurulum:
```bash
pip install -r gereklilikler.txt
```

## Kodun Genel Yapısı

Ana dosya, bir ses dosyasının işlenmesi ve çıkarılan özelliklerin kaydedilmesi için gerekli fonksiyonları içerir.

### Fonksiyonlar

#### 1. `ses_dosyasi_yukle(dosya_yolu, sr=22050)`
Bu fonksiyon, belirli bir dosya yolundaki ses dosyasını belirtilen örnekleme frekansıyla (varsayılan: 22050 Hz) yükler.

- **Parametreler:**
  - `dosya_yolu` (str): Yüklenecek ses dosyasının yolu.
  - `sr` (int): Örnekleme frekansı.

- **Döndürülenler:**
  - `y` (ndarray): Ses verisi.
  - `sr` (int): Örnekleme frekansı.

#### 2. `gurultu_temizleme(y, sr)`
Gelişmiş spektral yöntemle gürültü azaltma işlemi yapar.

- **Parametreler:**
  - `y` (ndarray): Ses verisi.
  - `sr` (int): Örnekleme frekansı.

- **Döndürülenler:**
  - `temizlenmis_gurultu` (ndarray): Gürültüsü azaltılmış ses verisi.

#### 3. `sinyali_temizle(y)`
Sinyali kontrol eder ve sonsuz veya NaN değerleri sıfıra çevirir.

- **Parametreler:**
  - `y` (ndarray): Ses verisi.

- **Döndürülenler:**
  - `y` (ndarray): Temizlenmiş ses verisi.

#### 4. `ses_normalizasyonu(y)`
Ses verisini normalleştirir.

- **Parametreler:**
  - `y` (ndarray): Ses verisi.

- **Döndürülenler:**
  - `y` (ndarray): Normalleştirilmiş ses verisi.

#### 5. `mfcc_cikar(y, sr, n_mfcc=13)`
Ses verisinden MFCC özelliklerini çıkarır.

- **Parametreler:**
  - `y` (ndarray): Ses verisi.
  - `sr` (int): Örnekleme frekansı.
  - `n_mfcc` (int): Çıkarılacak MFCC sayısı.

- **Döndürülenler:**
  - `mfccs` (ndarray): MFCC özellikleri.

#### 6. `zero_crossing_rate_cikar(y)`
Sıfır geçiş oranını çıkarır.

- **Parametreler:**
  - `y` (ndarray): Ses verisi.

- **Döndürülenler:**
  - `zcr` (ndarray): Sıfır geçiş oranı.

#### 7. `chroma_features_cikar(y, sr)`
Kromatik özellikleri çıkarır.

- **Parametreler:**
  - `y` (ndarray): Ses verisi.
  - `sr` (int): Örnekleme frekansı.

- **Döndürülenler:**
  - `chroma` (ndarray): Kromatik özellikler.

#### 8. `ozellikleri_gorsellestir(mfccs, zcr, chroma, sr, cikti_dosya_adi)`
Özelliklerin görselleştirilmesi ve belirtilen dosyaya kaydedilmesi işlemini gerçekleştirir.

- **Parametreler:**
  - `mfccs` (ndarray): MFCC özellikleri.
  - `zcr` (ndarray): Sıfır geçiş oranı.
  - `chroma` (ndarray): Kromatik özellikler.
  - `sr` (int): Örnekleme frekansı.
  - `cikti_dosya_adi` (str): Görselleştirmenin kaydedileceği dosya yolu.

#### 9. `ses_dosyasi_isle(dosya_yolu, gurultu_cikti_klasoru, npy_cikti_klasoru, csv_cikti_klasoru, png_cikti_klasoru)`
Tek bir ses dosyasını işler, gürültüyü azaltır, özellik çıkarır ve sonuçları belirli klasörlere kaydeder.

- **Parametreler:**
  - `dosya_yolu` (str): İşlenecek ses dosyasının yolu.
  - `gurultu_cikti_klasoru` (str): Gürültüsü azaltılmış dosyaların kaydedileceği klasör.
  - `npy_cikti_klasoru` (str): MFCC özelliklerinin `.npy` formatında kaydedileceği klasör.
  - `csv_cikti_klasoru` (str): Özelliklerin CSV formatında kaydedileceği klasör.
  - `png_cikti_klasoru` (str): Özelliklerin görselleştirilmesinin kaydedileceği klasör.

#### 10. `ses_isle_klasor(giris_klasoru, gurultu_cikti_klasoru, npy_cikti_klasoru, csv_cikti_klasoru, png_cikti_klasoru)`
Belirtilen klasördeki tüm MP3 dosyalarını işleyerek sonuçları ilgili klasörlere kaydeder.

- **Parametreler:**
  - `giris_klasoru` (str): MP3 dosyalarının bulunduğu klasör.
  - `gurultu_cikti_klasoru` (str): Gürültüsü azaltılmış dosyaların kaydedileceği klasör.
  - `npy_cikti_klasoru` (str): MFCC özelliklerinin `.npy` formatında kaydedileceği klasör.
  - `csv_cikti_klasoru` (str): Özelliklerin CSV formatında kaydedileceği klasör.
  - `png_cikti_klasoru` (str): Özelliklerin görselleştirilmesinin kaydedileceği klasör.

## Kullanım

Kullanım örneği:

1. İşlem yapılacak dosyaların bulunduğu klasörü ve çıktıların kaydedileceği klasör yollarını ayarlayın.
2. `ses_isle_klasor` fonksiyonunu çağırarak tüm MP3 dosyalarını işleyin:

```python
giris_klasoru = r"C:\Users\Niyazi\Desktop\onislenmis-veri\ingilizce\ingilizce-ham"
gurultu_cikti_klasoru = r"C:\Users\Niyazi\Desktop\onislenmis-veri\ingilizce\ingilizce_gurultu_temizleme"
npy_cikti_klasoru = r"C:\Users\Niyazi\Desktop\onislenmis-veri\ingilizce\ingilizce_npy"
csv_cikti_klasoru = r"C:\Users\Niyazi\Desktop\onislenmis-veri\ingilizce\ingilizce_csv"
png_cikti_klasoru = r"C:\Users\Niyazi\Desktop\onislenmis-veri\ingilizce\ingilizce_png"

# Tüm MP3 dosyalarını işle
ses_isle_klasor(giris_klasoru, gurultu_cikti_klasoru, npy_cikti_klasoru, csv_cikti_klasoru, png_cikti_klasoru)
```

### Çıktılar

- **Gürültüsü Azaltılmış Ses Dosyaları:** Belirtilen `gurultu_cikti_klasoru` klasöründe `.wav` formatında kaydedilir.
- **MFCC Özellikleri:** `npy_cikti_klasoru` klasöründe `.npy` formatında saklanır.
- **Özellikler CSV Dosyası:** `csv_cikti_klasoru `klasöründe `.csv` formatında kaydedilir.
- **Özellikler Görselleştirmesi:** `png_cikti_klasoru` klasöründe `.png` formatında kaydedilir.

