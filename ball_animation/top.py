"""
TOP SINIFI
==========
Ekranda hareket eden renkli daireleri temsil eden sınıf.
Her top kendi konumunu, rengini ve hareket hızını bilir.
"""

import pygame
import random
from config import MIN_HIZ, MAX_HIZ, TOP_GUVENLIK_MESAFESI


class Top:
    """
    Tek bir top objesi.
    
    Bu sınıf bir topun nasıl davranacağını belirler:
    - Ekranda belli bir yerde başlar
    - Rastgele yönde hareket eder
    - Kenarlara çarpınca seker
    """
    
    def __init__(self, x, y, boyut, renk, hiz_carpani=1):
        """
        Top oluşturulur. Başlangıç konumu, boyutu ve rengi ayarlanır.
        
        x, y: Ekrandaki konum (x yatay, y dikey)
        boyut: Topun ne kadar büyük olacağı (yarıçap)
        renk: (255, 0, 0) gibi kırmızı, mavi gibi RGB renk kodu
        hiz_carpani: Hız çarpanı - 1 normal hız
        """
        # Topun temel özellikleri
        self.x = x                          # Ekranda nerede (yatay)
        self.y = y                          # Ekranda nerede (dikey)
        self.boyut = boyut                   # Ne kadar büyük
        self.renk = renk                     # Hangi renk
        self.hiz_carpani = hiz_carpani      # Hız çarpanı (1 = normal)
        
        # Topu hareket ettirecek hız değerleri
        # Rastgele -1 veya +1 seçer (sola veya sağa)
        # Sonra MIN_HIZ ile MAX_HIZ arasında bir hız seçer
        self.hiz_x = random.choice([-1, 1]) * random.uniform(MIN_HIZ, MAX_HIZ) * self.hiz_carpani
        self.hiz_y = random.choice([-1, 1]) * random.uniform(MIN_HIZ, MAX_HIZ) * self.hiz_carpani
        
        self.hareket_ediyor = False  # Şu an hareket ediyor mu? (False = durmuş)

    def guncelle(self, cizim_alani):
        """
        Her karede çağrılır. Topun yerini biraz ilerletir.
        
        cizim_alani: Topların içinde hareket edeceği dikdörtgen alan
        """
        if self.hareket_ediyor:  # Eğer hareket ediyorsa
            # Topu biraz hareket ettir
            self.x += self.hiz_x  # Yatay olarak
            self.y += self.hiz_y  # Dikey olarak

            # SOL KENAR - Top çok sola gitti mi?
            if self.x - self.boyut < cizim_alani.x:
                self.x = cizim_alani.x + self.boyut    # Geri getir
                self.hiz_x = -self.hiz_x                     # Yönünü değiştir (sağa dön)
            
            # SAĞ KENAR - Top çok sağa gitti mi?
            elif self.x + self.boyut > cizim_alani.x + cizim_alani.width:
                self.x = cizim_alani.x + cizim_alani.width - self.boyut  # Geri getir
                self.hiz_x = -self.hiz_x  # Yönünü değiştir (sola dön)

            # ÜST KENAR - Top çok yukarıya gitti mi?
            if self.y - self.boyut < cizim_alani.y:
                self.y = cizim_alani.y + self.boyut    # Geri getir
                self.hiz_y = -self.hiz_y                     # Yönünü değiştir (aşağı dön)
            
            # ALT KENAR - Top çok aşağıya gitti mi?
            elif self.y + self.boyut > cizim_alani.y + cizim_alani.height:
                self.y = cizim_alani.y + cizim_alani.height - self.boyut  # Geri getir
                self.hiz_y = -self.hiz_y  # Yönünü değiştir (yukarı dön)

    def ciz(self, ekran, kaydirma_x=0, kaydirma_y=0):
        """
        Topu ekrana çizer (gösterir).
        
        ekran: Nereye çizeceğimiz
        kaydirma: Ekstra kaydırma (kullanmıyoruz aslında)
        """
        # pygame ile daire çiz
        pygame.draw.circle(ekran, self.renk, (int(self.x + kaydirma_x), int(self.y + kaydirma_y)), int(self.boyut))

    def hizlan(self, artis):
        """
        Topun hızını artırır. Aynı yönde gitmeye devam eder.
        
        artis: Hız ne kadar artacak (örn: 0.1 = %10 artış)
        """
        self.hiz_carpani += artis
        
        # X yönünde hızı artır
        if self.hiz_x != 0:
            # Yönünü koru ama hızı artır
            self.hiz_x = (self.hiz_x / abs(self.hiz_x)) * abs(self.hiz_x) * (1 + artis)
        
        # Y yönünde hızı artır
        if self.hiz_y != 0:
            self.hiz_y = (self.hiz_y / abs(self.hiz_y)) * abs(self.hiz_y) * (1 + artis)
