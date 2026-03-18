# 🔧 Koduğum Kodunu Kurtar (KKK) - V4

![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)
![VS Code Local History](https://img.shields.io/badge/VS%20Code-Local%20History-blueviolet.svg)
![License MIT](https://img.shields.io/badge/license-MIT-green.svg)

"Git restore çektim, her şey silindi!" dediğiniz o korkunç anda devreye giren, VS Code'un gizli yerel geçmişini (Local History) kullanarak projelerinizi saniyeler içinde eski haline döndüren bir acil durum terminal aracıdır.

## 🚀 Öne Çıkan Özellikler

*   🌍 **Global Timeline:** Tüm projeyi tek bir saniyeye (snapshot) geri döndürme.
*   🔍 **Dosya Bazlı Arama:** İsimle dosya arama ve o dosyanın tüm geçmiş versiyonlarını listeleme.
*   📝 **Grep Mode (İçerikle Arama):** Dosya adını unutsanız bile kodun içindeki bir fonksiyondan veya değişimden dosyayı bulma.
*   📊 **Diff Özetleri:** Versiyonlar arasındaki satır değişimlerini (+/-) geri yüklemeden önce görme.
*   🛡️ **Otomatik Yedekleme:** Geri yüklenen her dosyanın orijinal halini `.bak` olarak saklama.
*   📟 **Sayfalamalı Navigasyon:** Çok yoğun çalışma günlerinde bile geçmişte kolayca gezinme.

## 🛠️ Kolay Kurulum

### Linux & macOS
Terminali açın ve repoyu indirdiğiniz klasörde şu komutu çalıştırın:
```bash
git clone https://github.com/OmerFaruk-Celik/KKK.git
cd KKK
chmod +x install.sh && ./install.sh
source ~/.bashrc  # veya source ~/.zshrc
```

### Windows
PowerShell'i Yönetici olarak açın ve repoyu indirdiğiniz klasörde şu komutu çalıştırın:
```powershell
git clone https://github.com/OmerFaruk-Celik/KKK.git
cd KKK
Set-ExecutionPolicy Bypass -Scope Process -Force; ./install.ps1
```
*(Not: Kurulumdan sonra terminali kapatıp açmanız yeterlidir.)*

## 📖 Kullanım Rehberi

Terminali proje klasörünüzde açın ve `kkk` komutunu çalıştırın.

### Seçenek 1: Global Timeline (Zaman Makinesi)
Özellikle `git restore .` gibi tüm projeyi etkileyen kazalardan sonra kullanılır. Projenin 10 dakika veya 5 saat önceki "tüm dosyalar" halini listeler ve tek tuşla her şeyi geri getirir.

### Seçenek 2: Dosya Ara
Sadece tek bir dosyanın (örneğin `motor.py`) üzerinde çalışırken bir hata yaptıysanız, o dosyanın VS Code tarafından kaydedilmiş tüm eski sürümlerini tarihe göre listeler.

### Seçenek 3: Kod İçinde Ara (Grep Mode)
"Bir fonksiyon yazmıştım ama hangi dosyadaydı ve ne zaman silindi hatırlamıyorum" dediğinizde kullanılır. Kod parçacığını aratın, KKK size o kodun geçtiği tüm geçmiş versiyonları getirsin.

## ⚠️ Gereksinimler & Uyumluluk

*   **İşletim Sistemi:** Linux, macOS veya Windows (VS Code History klasör yapısını kullanan sistemler).
*   **Editör:** Visual Studio Code (Yerel geçmiş özelliği açık olmalıdır - varsayılan olarak açıktır).
*   **Python:** 3.6+

## 🛡️ Güvenlik Notu

Bu araç mevcut dosyalarınızın üzerine yazar. Her ne kadar `.bak` yedekleri oluştursa da, her geri yükleme işleminden önce ne yaptığınızdan emin olmanız önerilir.

## 🤝 Katkıda Bulunma

Hataları bildirmekten veya yeni özellik önerileri için Pull Request göndermekten çekinmeyin!

*Bu araç, bir yazılımcının en karanlık anında (yanlışlıkla her şeyi sildiği an) geliştirilmiştir.*

**Geliştirici:** Ömer Faruk Çelik  
**İsim Babası:** Terminaldeki Çaresizlik 😂
