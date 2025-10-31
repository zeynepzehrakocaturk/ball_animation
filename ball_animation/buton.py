"""
BUTON SINIFLARI
================
Üç tür buton var:
1. Buton - Normal metin butonları (START, STOP, RESET gibi)
2. IkonButon - Top boyutunu seçmek için ikon gösteren butonlar
3. RenkButon - Top rengini seçmek için renkli butonlar
"""

import pygame


class Buton:
    """
    Basit bir dikdörtgen buton.
    
    Metin yazılı butonlar için kullanılır.
    Örnek: "BAŞLA", "DUR", "SIFIRLA" butonları
    """
    
    def __init__(self, x, y, genislik, yukseklik, metin, renk, kenarlik_rengi=None):
        """
        Buton oluştur.
        
        x, y: Ekranın neresinde gözükecek
        genislik, yukseklik: Ne kadar büyük olacak
        metin: Üzerinde ne yazı olsun
        renk: Arka plan rengi
        kenarlik_rengi: Kenarlık rengi (yoksa siyah)
        """
        # Butonun dikdörtgen alanını oluştur
        self.dikdortgen = pygame.Rect(x, y, genislik, yukseklik)
        self.metin = metin                    # Ne yazıyor
        self.renk = renk                      # Hangi renk
        self.kenarlik_rengi = kenarlik_rengi or (0, 0, 0)  # Kenarlık (varsayılan siyah)
        self.basili_mi = False                        # Şu an basılı mı?

    def ciz(self, ekran, yazi_tipi):
        """
        Butonu ekrana çizdir.
        
        ekran: Nereye çizeceğiz
        yazi_tipi: Yazı nasıl görünecek
        """
        # Önce dikdörtgen çiz
        pygame.draw.rect(ekran, self.renk, self.dikdortgen)
        
        # Kenarlık ekle
        pygame.draw.rect(ekran, self.kenarlik_rengi, self.dikdortgen, 2)
        
        # Eğer metin varsa, onu da çiz
        if self.metin:
            yazi_yuzeyi = yazi_tipi.render(self.metin, True, self.kenarlik_rengi)
            yazi_konumu = yazi_yuzeyi.get_rect(center=self.dikdortgen.center)
            ekran.blit(yazi_yuzeyi, yazi_konumu)

    def tiklandi_mi(self, pozisyon):
        """
        Bu butona tıklandı mı kontrol et.
        
        pozisyon: Fare nerede (x, y)
        
        Döner: True = tıklandı, False = tıklanmadı
        """
        # collidepoint: Fare pozisyonu bu dikdörtgenin içinde mi?
        return self.dikdortgen.collidepoint(pozisyon)


class IkonButon(Buton):
    """
    İkon gösteren buton.
    
    Top boyutunu seçmek için kullanılır.
    Buton üzerinde daire şeklinde ikon var, büyüklüğü seçilen boyutu gösteriyor.
    """
    
    def __init__(self, x, y, genislik, yukseklik, boyut, renk, maks_boyut, kenarlik_rengi=None):
        """
        İkon butonu oluştur.
        
        x, y, genislik, yukseklik: Butonun konumu ve boyutu
        boyut: Bu buton hangi boyutu temsil ediyor (15, 30, 50 gibi)
        renk: İkonun rengi
        maks_boyut: En büyük boyut (ikonu ölçeklemek için)
        kenarlik_rengi: Kenarlık rengi
        """
        # Buton sınıfının init fonksiyonunu çağır
        super().__init__(x, y, genislik, yukseklik, "", renk, kenarlik_rengi)
        self.boyut = boyut        # Bu buton hangi boyutu gösteriyor
        self.maks_boyut = maks_boyut  # En büyük boyut

    def ciz(self, ekran, yazi_tipi):
        """
        İkon butonunu ekrana çiz.
        
        Daire şeklinde ikon çizer, seçiliyse ekstra bir çerçeve gösterir.
        """
        # İkonun en büyük ne kadar olabileceğini hesapla
        maks_ikon_yaricapi = min(self.dikdortgen.width, self.dikdortgen.height) // 2 - 6
        
        # İkonun gerçek yarıçapını hesapla (boyut oranına göre)
        # Küçük boyut = küçük ikon, büyük boyut = büyük ikon
        ikon_yaricapi = max(6, int(maks_ikon_yaricapi * (self.boyut / self.maks_boyut)))
        
        # İkonu çiz (daire)
        pygame.draw.circle(ekran, self.renk, self.dikdortgen.center, ikon_yaricapi)
        
        # İkonun kenarlığını çiz
        pygame.draw.circle(ekran, self.kenarlik_rengi, self.dikdortgen.center, ikon_yaricapi, 2)
        
        # Eğer seçiliyse, ekstra vurgu çiz
        if self.basili_mi:
            pygame.draw.circle(ekran, self.kenarlik_rengi, self.dikdortgen.center, ikon_yaricapi + 6, 4)


class RenkButon(Buton):
    """
    Renk gösteren buton.
    
    Top rengini seçmek için kullanılır.
    Buton hangi rengi gösteriyorsa o renk topun rengi olur.
    """
    
    def __init__(self, x, y, genislik, yukseklik, renk, kenarlik_rengi=None):
        """
        Renk butonu oluştur.
        
        x, y, genislik, yukseklik: Butonun konumu ve boyutu
        renk: Butonun gösterdiği renk (top bu renkte olacak)
        kenarlik_rengi: Kenarlık rengi
        """
        # Buton sınıfının init fonksiyonunu çağır
        super().__init__(x, y, genislik, yukseklik, "", renk, kenarlik_rengi)

    def ciz(self, ekran, yazi_tipi):
        """
        Renk butonunu ekrana çiz.
        
        Önce normal butonu çiz, sonra eğer seçiliyse ekstra kalın çerçeve ekle.
        """
        # Normal buton çizimi
        super().ciz(ekran, yazi_tipi)
        
        # Eğer seçiliyse, kalın çerçeve ekle
        if self.basili_mi:
            pygame.draw.rect(ekran, self.kenarlik_rengi, self.dikdortgen, 4)
