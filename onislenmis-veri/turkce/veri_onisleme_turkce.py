import os
import librosa
import numpy as np
import noisereduce as nr
import matplotlib.pyplot as plt
import soundfile as sf
import librosa.display
import csv

# Ses dosyasını yükleme ve örnekleme frekansı ayarlama
def ses_dosyasi_yukle(dosya_yolu, sr=22050):
    try:
        print(f"Ses dosyası yükleniyor: {dosya_yolu}")
        y, sr = librosa.load(dosya_yolu, sr=sr) # Ses dosyasını yükler
        return y, sr
    except Exception as h:
        print(f"{dosya_yolu} yüklenirken hata oluştu: {h}")
        return None, None # Hata durumunda None döner

# Gürültü temizleme 
def gurultu_temizleme(y, sr):
    try:
        print("gürültü temizleme işlemi başlatılıyor...")
        # Gürültü örneği olarak sesin ilk 0.5 saniyesini alıyoruz
        gurultu_ornegi = y[0:int(sr * 0.5)]  # İlk 0.5 saniyelik kısmı gürültü örneği olarak kullanıyoruz
        # Gürültü azaltma işlemi
        temizlenmis_gurultu = nr.reduce_noise(y=y, sr=sr, prop_decrease=0.95, y_noise=gurultu_ornegi, 
                                               stationary=False, n_std_thresh_stationary=2.0)
        return temizlenmis_gurultu
    except Exception as h:
        print(f"Gürültü temizleme sırasında hata oluştu: {h}")
        return y # Hata durumunda orijinal ses verisi döner

# Sinyali kontrol et ve sonsuz veya NaN (Sayısal olmayan) değerleri sıfırla
def sinyali_temizle(y):
    try:
        if not np.all(np.isfinite(y)):  # NaN veya sonsuz değerleri kontrol et
            print("Uyarı: Sinyal NaN veya sonsuz değerler içeriyor. Bunlar sıfır ile değiştirilecektir.")
            y = np.nan_to_num(y)  # NaN ve sonsuz değerleri sıfırla
        return y
    except Exception as h:
        print(f"Sinyal temizleme sırasında hata oluştu: {h}")
        return y # Hata durumunda orijinal sinyal döner

# Ses normalizasyonu
def ses_normalizasyonu(y):
    try:
        print("Ses normalizasyonu yapılıyor")
        y = sinyali_temizle(y) # Sinyali temizler (NaN ve sonsuz değerleri sıfırlar)
        return librosa.util.normalize(y)  # Sesin genliğini normalize et
    except Exception as h:
        print(f"Ses normalizasyonu sırasında hata oluştu: {h}")
        return   # Hata durumunda orijinal ses verisi döner

# MFCC (Mel-Frequency Cepstral Coefficients) çıkarma
def mfcc_cikar(y, sr, n_mfcc=13):
    try:
        print("MFCC özellikleri çıkarılıyor")
        return librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc) # MFCC çıkarımı
    except Exception as h:
        print(f"MFCC çıkarma sırasında hata oluştu: {h}")
        return None # Hata durumunda None döner

# Zero-Crossing Rate çıkarma
def zero_crossing_rate_cikar(y):
    try:
        print("Zero-Crossing Rate çıkarılıyor")
        return librosa.feature.zero_crossing_rate(y)[0] # Zero-Crossing Rate çıkarımı
    except Exception as h:
        print(f"Zero-Crossing Rate çıkarma sırasında hata oluştu: {h}")
        return None  # Hata durumunda None döner

# Chroma Features çıkarma
def chroma_features_cikar(y, sr):
    try:
        print("Chroma features çıkarılıyor")
        return librosa.feature.chroma_stft(y=y, sr=sr) # Chroma features çıkarımı
    except Exception as h:
        print(f"Chroma features çıkarma sırasında hata oluştu: {h}")
        return None  # Hata durumunda None döner

# MFCC, Zero-Crossing Rate ve Chroma Özelliklerini görselleştirme ve kaydetme
def ozellikleri_gorsellestir(mfccs, zcr, chroma, sr, cikti_dosya_adi):
    try:
        print(f"Özellikler çiziliyor ve {cikti_dosya_adi} dosyasına kaydediliyor")
        plt.figure(figsize=(10, 8))

        # MFCC grafiği
        plt.subplot(3, 1, 1)
        librosa.display.specshow(mfccs, sr=sr, x_axis='time')
        plt.colorbar()
        plt.title('MFCC')

        # Zero-Crossing Rate grafiği
        plt.subplot(3, 1, 2)
        plt.plot(zcr)
        plt.title('Zero-Crossing Rate')

        # Chroma Features grafiği
        plt.subplot(3, 1, 3)
        librosa.display.specshow(chroma, sr=sr, x_axis='time', y_axis='chroma')
        plt.colorbar()
        plt.title('Chroma Features')

        # Görselleştirmeyi kaydet
        plt.tight_layout()
        plt.savefig(cikti_dosya_adi)
        plt.close()
    except Exception as h:
        print(f"Özellikleri çizme sırasında hata oluştu: {h}")

# Ses dosyası işleme ve sonuçları belirli klasörlere kaydetme
def ses_dosyasi_isle(dosya_yolu, gurultu_cikti_klasoru, npy_cikti_klasoru, csv_cikti_klasoru, png_cikti_klasoru):
    try:
        # Dosya adından uzantıyı çıkararak temel dosya adını alıyoruz
        cikti_dosya_temel_ad = os.path.splitext(os.path.basename(dosya_yolu))[0]

        # Ses dosyasını yükle
        y, sr = ses_dosyasi_yukle(dosya_yolu)
        if y is None:
            return

        # Gürültü temizleme
        y_gurultu_temizlenmis = gurultu_temizleme(y, sr)
        # Ses normalizasyonu
        y_normalize = ses_normalizasyonu(y_gurultu_temizlenmis)

        # MFCC, Zero-Crossing Rate ve Chroma features çıkar
        mfccs = mfcc_cikar(y_normalize, sr)
        zcr = zero_crossing_rate_cikar(y_normalize)
        chroma = chroma_features_cikar(y_normalize, sr)

        # Eğer MFCC, zcr veya Chroma features biri çıkmadıysa işlemi sonlandır
        if mfccs is None or zcr is None or chroma is None:
            return

        # Dosya adları oluşturma
        gurultu_temizlenmis_dosya_yolu = os.path.join(gurultu_cikti_klasoru, cikti_dosya_temel_ad + '_denoised.wav')
        mfcc_dosya_yolu = os.path.join(npy_cikti_klasoru, cikti_dosya_temel_ad + '_mfcc.npy')
        features_csv_yolu = os.path.join(csv_cikti_klasoru, cikti_dosya_temel_ad + '_features.csv')
        features_resim_yolu = os.path.join(png_cikti_klasoru, cikti_dosya_temel_ad + '_features.png')
        
        # Gürültü temizlenmiş ses dosyasını kaydetme
        print(f"Gürültü temizlenmiş ses dosyası kaydediliyor: {gurultu_temizlenmis_dosya_yolu}")
        sf.write(gurultu_temizlenmis_dosya_yolu, y_normalize, sr)

        # MFCC verisini kaydetme
        print(f"MFCC verisi kaydediliyor: {mfcc_dosya_yolu}")
        np.save(mfcc_dosya_yolu, mfccs)

        # Özellikleri CSV dosyasına kaydetme
        print(f"Özellikler CSV dosyasına kaydediliyor: {features_csv_yolu}")
        with open(features_csv_yolu, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['MFCC', 'Zero-Crossing Rate', 'Chroma Features'])
            for i in range(min(len(mfccs[0]), len(zcr), chroma.shape[1])):
                writer.writerow([mfccs[0][i], zcr[i], chroma[:, i].tolist()])
        
        # Özelliklerin görselleştirilmesini kaydetme
        ozellikleri_gorsellestir(mfccs, zcr, chroma, sr, features_resim_yolu)

        print(f"{cikti_dosya_temel_ad} için işlemler tamamlandı.")
    except Exception as h:
        print(f"{dosya_yolu} işlenirken hata oluştu: {h}")

# Klasördeki tüm MP3 dosyalarını işleme
def ses_isle_klasor(giris_klasoru, gurultu_cikti_klasoru, npy_cikti_klasoru, csv_cikti_klasoru, png_cikti_klasoru):
    # Çıktı klasörlerini oluşturma (varsa atla, yoksa oluştur)
    for klasor in [gurultu_cikti_klasoru, npy_cikti_klasoru, csv_cikti_klasoru, png_cikti_klasoru]:
        if not os.path.exists(klasor):
            os.makedirs(klasor)  # Klasör yoksa oluşturuluyor
            print(f"Çıktı klasörü oluşturuldu: {klasor}")

    # Klasördeki dosyaları tarama
    for root, dirs, files in os.walk(giris_klasoru):
        for file_name in files:
            if file_name.endswith('.mp3'):  # Yalnızca MP3 dosyaları işleniyor
                dosya_yolu = os.path.join(root, file_name)
                print(f"İşleniyor: {dosya_yolu}")
                ses_dosyasi_isle(dosya_yolu, gurultu_cikti_klasoru, npy_cikti_klasoru, csv_cikti_klasoru, png_cikti_klasoru)

# Klasör yolları
giris_klasoru = r"C:\Users\Niyazi\Desktop\onislenmis-veri\turkce\turkce-ham"
gurultu_cikti_klasoru = r"C:\Users\Niyazi\Desktop\onislenmis-veri\turkce\turkce_gurultu_temizleme"
npy_cikti_klasoru = r"C:\Users\Niyazi\Desktop\onislenmis-veri\turkce\turkce_npy"
csv_cikti_klasoru = r"C:\Users\Niyazi\Desktop\onislenmis-veri\turkce\turkce_csv"
png_cikti_klasoru = r"C:\Users\Niyazi\Desktop\onislenmis-veri\turkce\turkce_png"

# Tüm MP3 dosyalarını işleme
ses_isle_klasor(giris_klasoru, gurultu_cikti_klasoru, npy_cikti_klasoru, csv_cikti_klasoru, png_cikti_klasoru)
