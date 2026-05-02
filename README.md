<p align="center">
  <h1>Ball Animation Game</h1>
</p>

**Kısa Açıklama**

Ball Animation Game, basit bir top animasyonu ve etkileşimi sunan küçük bir Python projesidir. Bu README, geliştiriciler ve kullanıcılar için hızlı kurulum, çalıştırma, proje yapısı ve katkı rehberi içerir.

| Özellik | Detay |
|---|---|
| Durum | Tamamlandı (lokal prototip) |
| Dil | Python 3.8+ |
| Platform | Windows / Cross-platform (Python destekliyorsa) |
| Ana Dosyalar | `buton.py`, `config.py`, `main.py`, `top.py` |

**İçindekiler**

- [Kurulum](#kurulum)
- [Çalıştırma](#çalıştırma)
- [Kontroller ve Kullanım](#kontroller-ve-kullanım)
- [Proje Yapısı](#proje-yapısı)
- [Geliştirme & Katkı](#geliştirme--katkı)
- [Teknoloji ve CI](#teknoloji-ve-ci-önerisi)
- [Lisans](#lisans)

## Kurulum

1. Python 3.8 veya üstünü yükleyin.
2. (Önerilir) Sanal ortam oluşturun:

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

3. Gerekli bağımlılıklar varsa `requirements.txt` dosyasına ekleyip yükleyin:

```bash
pip install -r requirements.txt
```

Not: Projedeki mevcut dosyalar temel Python kodu içeriyorsa ekstra paket gerekmeyebilir.

## Çalıştırma

Projeyi başlatmak için:

```bash
python main.py
```

Uygulama Windows üzerinde PowerShell veya CMD ile çalıştırılabilir.

## Kontroller ve Kullanım

- Oyun/animasyon başlatıldığında ekranda top görülür.
- Kontroller ve davranış detayları `main.py` ve `buton.py` içinde açıklanmıştır.
- Eğer tuş atamaları veya davranışlar değiştirilmek istenirse `config.py` üzerinden ayarlama yapabilirsiniz.

## Proje Yapısı

| Dosya | Açıklama |
|---|---|
| `main.py` | Uygulama giriş noktası; pencere oluşturma, döngü ve olay yönetimi |
| `top.py` | Top sınıfı/animasyonu: konum, hız, çarpışma mantığı |
| `buton.py` | UI butonları ve etkileşim yardımcıları |
| `config.py` | Konfigürasyon: renkler, hız, pencere boyutu gibi ayarlar |

## Geliştirme & Katkı

- Fork → Branch → PR iş akışını kullanın.
- Kod formatı: `black` ile formatlayın; statik analiz için `flake8` önerilir.
- Yeni özellik eklerken küçük, test edilebilir commitler yapın ve açıklayıcı commit mesajları ekleyin.

PR ve issue açarken lütfen aşağıdakileri paylaşın:

- Hata/özellik açıklaması
- Yeniden üretme adımları
- Beklenen ve gerçekleşen davranış

## Teknoloji ve CI 

- Dil: `Python 3.8+`
- Kod formatlama: `black`  
- Linting: `flake8` veya `ruff`  


## Lisans

Bu proje MIT lisansı ile lisanslanmıştır. Detay için `LICENSE` dosyası ekleyin.
