"""
ANA OYUN DOSYASI (MAIN.PY)
============================
Bu dosya oyunun ana döngüsünü ve kullanıcı etkileşimlerini yönetir.

Oyun Nasıl Çalışır:
1. Kullanıcı bir BOYUT seçer (küçük, orta, büyük)
2. Kullanıcı bir RENK seçer (kırmızı, mavi, sarı)
3. Hem boyut hem renk seçili olduğunda, herhangi birine tekrar tıklayınca TOP OLUŞUR
4. START butonuna basınca toplar HAREKET EDER
5. STOP ile durdurulur, RESET ile temizlenir
6. Speed Up ile topların hızı artırılır
"""

import pygame
import random
from config import *
from top import Top
from buton import Buton, IkonButon, RenkButon


def oyunu_baslat():
    """
    Oyun ekranını hazırlar ve başlangıç nesnelerini oluşturur.
    
    Döner:
        screen: Oyun ekranı (yüzey)
        clock: Oyunun hızını kontrol eden saat nesnesi
        font: Butonlardaki yazılar için font
    """
    pygame.init()  # Pygame kütüphanesini başlat
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # 1200x800 boyutunda pencere oluştur
    pygame.display.set_caption("Ball Animation")  # Pencere başlığını ayarla
    clock = pygame.time.Clock()  # FPS kontrolü için saat oluştur
    font = pygame.font.Font(None, 24)  # Varsayılan font, 24 boyutunda
    return screen, clock, font


def boyut_butonlari_olustur(x_baslangic, y_ust_satir, boyut_degerleri):
    """
    Boyut seçim butonlarını oluşturur (daire ikonlar).
    
    Parametreler:
        x_start: Butonların başlangıç X konumu
        y_top_row: Üst satırın Y konumu
        size_values: Top boyutları listesi [15, 30, 50]
    
    Döner:
        size_buttons: Oluşturulan butonların listesi
    """
    BUTON_KUTUSU = 70      # Her buton 70x70 piksel
    BUTON_BOSLUK = 20      # Butonlar arası boşluk
    boyut_butonlari_listesi = []
    en_buyuk_boyut = max(boyut_degerleri)  # En büyük boyut (ölçekleme için)
    
    # Her boyut için bir buton oluştur
    for i, boyut in enumerate(boyut_degerleri):
        # X pozisyonunu hesapla: Başlangıç + (Buton boyutu + Boşluk) * İndis
        x_pozisyonu = x_baslangic + i * (BUTON_KUTUSU + BUTON_BOSLUK)
        # İkon butonu oluştur (boyut bilgisi ile)
        buton = IkonButon(x_pozisyonu, y_ust_satir, BUTON_KUTUSU, BUTON_KUTUSU, boyut, GRİ, en_buyuk_boyut, SIYAH)
        boyut_butonlari_listesi.append(buton)
    
    return boyut_butonlari_listesi


def renk_butonlari_olustur(x_baslangic, y_ust_satir, boyut_degerleri):
    """
    Renk seçim butonlarını oluşturur.
    
    Parametreler:
        x_start: Başlangıç X konumu
        y_top_row: Üst satır Y konumu
        size_values: Boyut değerleri (butonların yerini belirlemek için)
    
    Döner:
        color_buttons: Oluşturulan renk butonlarının listesi
    """
    renk_butonlari = []
    renkler = [KIRMIZI, MAVI, SARI]  # Kırmızı, mavi, sarı
    COLOR_BOX = 50       # Renk butonları 50x50 piksel
    ICON_BOX = 70       # Boyut butonları boyutu (referans için)
    ICON_SPACING = 20   # Boşluk
    
    # Renk butonlarının başlangıç X pozisyonu (boyut butonlarının yanında)
    baslangic_x_renk = x_baslangic + len(boyut_degerleri) * (ICON_BOX + ICON_SPACING) + 20
    
    # Her renk için bir buton oluştur
    for i, renk in enumerate(renkler):
        x_pos = baslangic_x_renk + i * (COLOR_BOX + 20)  # X pozisyonu
        y_pos = y_ust_satir + (ICON_BOX - COLOR_BOX) // 2  # Dikey ortala
        btn = RenkButon(x_pos, y_pos, COLOR_BOX, COLOR_BOX, renk, SIYAH)
        renk_butonlari.append(btn)
    
    return renk_butonlari


def kontrol_butonlari_olustur(x_baslangic, y_alt_satir):
    """
    Kontrol butonlarını oluştur (BAŞLA, DUR, SIFIRLA, HIZLAN).
    
    Parametreler:
        x_baslangic: Başlangıç X konumu
        y_alt_satir: Alt satır Y konumu
    
    Döner:
        (Metin butonları listesi, Hızlandır butonu)
    """
    # Buton verileri: (Yazı, Renk)
    buton_verileri = [
        ("START", KIRMIZI),    # START butonu kırmızı
        ("STOP", MAVI),    # STOP butonu mavi
        ("RESET", SARI)  # RESET butonu sarı
    ]
    
    # Butonların X konumları
    buton_x_konumlari = [x_baslangic, x_baslangic + 130, x_baslangic + 260]
    metin_butonlari_liste = []
    
    # Her buton için buton oluştur
    for i, (metin, renk) in enumerate(buton_verileri):
        metin_butonu = Buton(buton_x_konumlari[i] - 20, y_alt_satir + 45, 75, 30, metin, BEYAZ, SIYAH)
        metin_butonlari_liste.append(metin_butonu)
    
    # Hızlandır butonu (sağ üstte)
    hizlandir_butonu = Buton(SCREEN_WIDTH - 150, y_alt_satir + 20, 100, 30, "SPEED UP", BEYAZ, SIYAH)
    return metin_butonlari_liste, hizlandir_butonu


def topu_guvenli_olustur(toplar, boyut, renk, cizim_alani, animasyon_calisiyor):
    """
    Topu ekranın kenarlarından uzak, güvenli bir konumda oluşturur.
    
    Parametreler:
        balls: Mevcut top listesi (yeni top eklenecek)
        size: Topun yarıçapı
        color: Topun rengi
        drawing_area: Topların hareket edeceği alan
        animation_running: Animasyon çalışıyor mu? (yeni top başlasın mı?)
    
    Döner:
        Güncellenmiş top listesi
    """
    # Topun başlayabileceği güvenli alanı hesapla
    # Kenarlardan TOP_GUVENLIK_MESAFESI kadar içeride başlar
    min_x = cizim_alani.x + boyut + TOP_GUVENLIK_MESAFESI        # Sol kenar + güvenlik
    max_x = cizim_alani.x + cizim_alani.width - boyut - TOP_GUVENLIK_MESAFESI  # Sağ kenar - güvenlik
    min_y = cizim_alani.y + boyut + TOP_GUVENLIK_MESAFESI        # Üst kenar + güvenlik
    max_y = cizim_alani.y + cizim_alani.height - boyut - TOP_GUVENLIK_MESAFESI # Alt kenar - güvenlik
    
    # Güvenli alan kontrolü (alan yeterli mi?)
    if min_x < max_x and min_y < max_y:
        # Rastgele güvenli bir konum seç
        rand_x = random.randint(int(min_x), int(max_x))
        rand_y = random.randint(int(min_y), int(max_y))
        
        # Yeni top oluştur
        yeni_top = Top(rand_x, rand_y, boyut, renk, 1)
        toplar.append(yeni_top)  # Listeye ekle
        
        # Eğer animasyon çalışıyorsa, bu top hemen harekete başlasın
        if animasyon_calisiyor:
            yeni_top.hareket_ediyor = True
    
    return toplar


def top_olustur_eger_secildi(secilen_boyut, secilen_renk, toplar, cizim_alani, 
                           animasyon_calisiyor, boyut_butonlari, renk_butonlari):
    """
    Eğer hem boyut hem renk seçilmişse, top oluşturur ve butonları temizler.
    
    Parametreler:
        selected_size: Seçili boyut (veya None)
        selected_color: Seçili renk (veya None)
        balls: Mevcut top listesi
        drawing_area: Çizim alanı
        animation_running: Animasyon durumu
        size_buttons: Boyut butonları listesi
        color_buttons: Renk butonları listesi
    
    Döner:
        Tuple: (seçili boyut, seçili renk, güncellenmiş top listesi)
    """
    # Hem boyut hem renk seçildi mi kontrol et
    if secilen_boyut is not None and secilen_renk is not None:
        # Top oluştur
        toplar = topu_guvenli_olustur(toplar, secilen_boyut, secilen_renk, cizim_alani, animasyon_calisiyor)
        
        # Tüm butonlardaki seçimi temizle (bir sonraki seçim için)
        for buton in boyut_butonlari:
            buton.basili_mi = False
        for buton in renk_butonlari:
            buton.basili_mi = False
        
        # Seçimleri sıfırla (böylece yeniden seçim yapılabilir)
        return None, None, toplar
    
    # Henüz seçim tamamlanmamışsa, mevcut seçimleri koru
    return secilen_boyut, secilen_renk, toplar


def kontrol_butonlarini_isle(fare_pozisyonu, metin_butonlari, hiz_artir_butonu, toplar, 
                           animasyon_calisiyor, hiz_carpani, boyut_butonlari, renk_butonlari):
    """
    Kontrol butonlarına tıklama işlemlerini yönetir.
    
    Butonlar:
    - START: Tüm topları harekete geçirir
    - STOP: Tüm topları durdurur
    - RESET: Tüm topları siler, butonları sıfırlar
    - Speed Up: Tüm topların hızını artırır
    
    Parametreler:
        mouse_pos: Fare pozisyonu
        text_buttons: START/STOP/RESET butonları
        speed_up_btn: Speed Up butonu
        balls: Top listesi
        animation_running: Animasyon çalışıyor mu?
        speed_multiplier: Hız çarpanı
        size_buttons, color_buttons: Butonları sıfırlamak için
    
    Döner:
        Tuple: (top listesi, animasyon durumu, hız çarpanı)
    """
    # Metin butonları kontrolü (BAŞLA, DUR, SIFIRLA)
    for buton in metin_butonlari:
        if buton.tiklandi_mi(fare_pozisyonu):
            # START butonu
            if buton.metin == "START":
                animasyon_calisiyor = True  # Animasyonu başlat
                for top in toplar:        # Tüm topları hareket ettir
                    top.hareket_ediyor = True
            
            # STOP butonu
            elif buton.metin == "STOP":
                animasyon_calisiyor = False  # Animasyonu durdur
                for top in toplar:        # Tüm topları durdur
                    top.hareket_ediyor = False
            
            # RESET butonu
            elif buton.metin == "RESET":
                toplar = []                    # Tüm topları sil
                hiz_carpani = 1          # Hızı sıfırla
                animasyon_calisiyor = False     # Animasyonu durdur
                
                # Tüm seçili butonları sıfırla
                for b in boyut_butonlari:
                    b.basili_mi = False
                for b in renk_butonlari:
                    b.basili_mi = False
    
    # HIZLAN butonu kontrolü
    if hiz_artir_butonu.tiklandi_mi(fare_pozisyonu):
        # Her topun hızını artır
        for top in toplar:
            top.hizlan(SPEED_INCREMENT)
    
    return toplar, animasyon_calisiyor, hiz_carpani


def toplari_guncelle(toplar, cizim_alani):
    """
    Tüm topları günceller (her karede çağrılır).
    
    Parametreler:
        balls: Top listesi
        drawing_area: Çizim alanı
    """
    for top in toplar:
        top.guncelle(cizim_alani)  # Her topun pozisyonunu güncelle


def oyunu_ciz(ekran, yazi_tipi, cizim_alani, toplar, boyut_butonlari, renk_butonlari, 
              metin_butonlari, hiz_artir_butonu):
    """
    Tüm oyun ekranını çizer (her karede çağrılır).
    
    Parametreler:
        screen: Ekran yüzeyi
        font: Font nesnesi
        drawing_area: Çizim alanı
        balls: Top listesi
        size_buttons: Boyut butonları
        color_buttons: Renk butonları
        text_buttons: Kontrol butonları
        speed_up_btn: Speed Up butonu
    """
    # Ekranı beyazla temizle
    ekran.fill(BEYAZ)
    
    # ÇİZİM ALANI (topların hareket ettiği bölge)
    pygame.draw.rect(ekran, ACIK_GRİ, cizim_alani)    # Arka plan
    pygame.draw.rect(ekran, SIYAH, cizim_alani, 2)     # Kenarlık
    
    # Topları çiz
    for top in toplar:
        top.ciz(ekran)
    
    # KONTROL PANELİ (butonların olduğu bölge)
    kontrol_paneli = pygame.Rect(0, DRAWING_AREA_HEIGHT, SCREEN_WIDTH, CONTROL_PANEL_HEIGHT)
    pygame.draw.rect(ekran, (232, 232, 232), kontrol_paneli)
    
    # Butonları çiz
    for buton in boyut_butonlari:
        buton.ciz(ekran, yazi_tipi)
    
    for buton in renk_butonlari:
        buton.ciz(ekran, yazi_tipi)
    
    for buton in metin_butonlari:
        buton.ciz(ekran, yazi_tipi)
    
    hiz_artir_butonu.ciz(ekran, yazi_tipi)


def main():
    """
    ANA OYUN DÖNGÜSÜ
    
    Bu fonksiyon:
    1. Oyunu başlatır
    2. Butonları oluşturur
    3. Kullanıcı etkileşimlerini dinler (fare tıklamaları)
    4. Her karede ekranı yeniden çizer
    5. 60 FPS ile sürekli çalışır
    
    Oyun penceresi kapatılıncaya kadar döngü devam eder.
    """
    # Oyunu başlat
    ekran, saat, yazi_tipi = oyunu_baslat()
    
    # BAŞLANGIÇ DURUMLARI
    cizim_alani = pygame.Rect(0, 0, SCREEN_WIDTH, DRAWING_AREA_HEIGHT)  # Çizim alanı (0,0) konumunda
    toplar = []                     # Henüz top yok
    secilen_boyut = None           # Henüz boyut seçilmedi
    secilen_renk = None          # Henüz renk seçilmedi
    animasyon_calisiyor = False      # Animasyon durmuş
    hiz_carpani = 1           # Normal hız
    
    # BUTON KONUMLARI
    y_ust_satir = DRAWING_AREA_HEIGHT + 25    # Boyut/renk butonlarının Y konumu
    y_alt_satir = DRAWING_AREA_HEIGHT + 100 # Kontrol butonlarının Y konumu
    x_baslangic = 50                              # Sol kenardan 50 piksel içeride
    boyut_degerleri = [15, 30, 50]               # Kullanılabilir top boyutları (yarıçap)
    
    # Butonları oluştur
    boyut_butonlari = boyut_butonlari_olustur(x_baslangic, y_ust_satir, boyut_degerleri)
    renk_butonlari = renk_butonlari_olustur(x_baslangic, y_ust_satir, boyut_degerleri)
    metin_butonlari, hiz_artir_butonu = kontrol_butonlari_olustur(x_baslangic, y_alt_satir)
    
    # ANA OYUN DÖNGÜSÜ - Oyun penceresi kapanana kadar devam et
    calisiyor = True
    while calisiyor:
        # OLayLARI KONTROL ET (fare tıklama, pencere kapatma vb.)
        for event in pygame.event.get():
            # Kullanıcı pencereyi kapatıyor mu?
            if event.type == pygame.QUIT:
                calisiyor = False  # Oyunu sonlandır
            
            # Fare ile bir butona tıklandı mı?
            elif event.type == pygame.MOUSEBUTTONDOWN:
                fare_pozisyonu = pygame.mouse.get_pos()  # Farenin nerede olduğunu al
                
                # Boyut seçen butonlara baktık mı?
                for buton in boyut_butonlari:
                    if buton.tiklandi_mi(fare_pozisyonu):  # Bu butona tıklandı mı?
                        secilen_boyut = buton.boyut    # Bu boyut seçildi
                        # Tüm boyut butonlarını kapat
                        for b in boyut_butonlari:
                            b.basili_mi = False
                        buton.basili_mi = True       # Sadece seçilen buton aktif
                        
                        # Hem boyut hem renk seçiliyse top yap
                        secilen_boyut, secilen_renk, toplar = top_olustur_eger_secildi(
                            secilen_boyut, secilen_renk, toplar, cizim_alani, 
                            animasyon_calisiyor, boyut_butonlari, renk_butonlari)
                
                # Renk seçen butonlara baktık mı?
                for buton in renk_butonlari:
                    if buton.tiklandi_mi(fare_pozisyonu):  # Bu butona tıklandı mı?
                        secilen_renk = buton.renk  # Bu renk seçildi
                        # Tüm renk butonlarını kapat
                        for b in renk_butonlari:
                            b.basili_mi = False
                        buton.basili_mi = True       # Sadece seçilen buton aktif
                        
                        # Hem boyut hem renk seçiliyse top yap
                        secilen_boyut, secilen_renk, toplar = top_olustur_eger_secildi(
                            secilen_boyut, secilen_renk, toplar, cizim_alani, 
                            animasyon_calisiyor, boyut_butonlari, renk_butonlari)
                
                # Kontrol butonlarını işle (BAŞLA, DUR, SIFIRLA, HIZLAN)
                toplar, animasyon_calisiyor, hiz_carpani = kontrol_butonlarini_isle(
                    fare_pozisyonu, metin_butonlari, hiz_artir_butonu, toplar, animasyon_calisiyor, 
                    hiz_carpani, boyut_butonlari, renk_butonlari)
        
        # Her karede topları hareket ettir
        toplari_guncelle(toplar, cizim_alani)
        
        # Her karede ekranı yeniden çiz
        oyunu_ciz(ekran, yazi_tipi, cizim_alani, toplar, boyut_butonlari, renk_butonlari, 
                  metin_butonlari, hiz_artir_butonu)
        
        # Ekranı güncelle (60 fps ile)
        pygame.display.flip()
        saat.tick(60)
    
    # Oyun bittiğinde Pygame'i kapat
    pygame.quit()


# Eğer bu dosya doğrudan çalıştırılırsa (python main.py)
# main() fonksiyonunu çağır
if __name__ == "__main__":
    main()
