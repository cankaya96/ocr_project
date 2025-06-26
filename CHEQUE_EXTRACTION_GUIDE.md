# Çek Bilgi Çıkarma Sistemi - Kullanım Kılavuzu

Bu sistem, `uploads/cheque` klasöründeki çek görüntülerinden Google Gemini AI kullanarak otomatik olarak bilgi çıkarır.

## 🚀 Hızlı Başlangıç

### 1. Gerekli Paketleri Yükleyin
```bash
pip install -r requirements_gemini.txt
```

### 2. Gemini API Anahtarı Alın
1. https://makersuite.google.com/app/apikey adresine gidin
2. Ücretsiz API anahtarınızı oluşturun
3. API anahtarını environment variable olarak ayarlayın:

**macOS/Linux:**
```bash
export GEMINI_API_KEY="your_api_key_here"
```

**Windows:**
```cmd
set GEMINI_API_KEY=your_api_key_here
```

### 3. Çek Bilgilerini Çıkarın
```bash
python extract_cheque_info.py
```

## 📊 Çıkarılan Bilgiler

Sistem her çek görüntüsünden şu bilgileri çıkarmaya çalışır:

| Alan | Açıklama | Örnek |
|------|----------|-------|
| `_fileName` | Dosya adı | `cheque_001.jpg` |
| `_iban` | IBAN numarası | `TR330006100519786457841326` |
| `_checkNo` | Çek numarası | `0001234567` |
| `_branchCode` | Şube kodu | `0519` |
| `_accountNumber` | Hesap numarası | `12345678` |
| `_tcknVkn` | TC/VKN numarası | `12345678901` |
| `_bankCode` | Banka kodu | `0061` |
| `_micrCode` | MICR kodu | `c0001234567c 0519c 0061c` |
| `_checkAmount` | Çek tutarı | `1500.00` |

## 📁 Sonuç Dosyası

Sonuçlar `cheque_extraction_results.json` dosyasına kaydedilir:

```json
[
  {
    "_fileName": "18961938218_26062025.jpg",
    "_iban": "TR330006100519786457841326",
    "_checkNo": "0001234567",
    "_branchCode": "0519",
    "_accountNumber": "12345678",
    "_tcknVkn": "18961938218",
    "_bankCode": "0061",
    "_micrCode": "c0001234567c 0519c 0061c",
    "_checkAmount": "1500.00"
  },
  {
    "_fileName": "22966699784_26062025.jpg",
    "_iban": null,
    "_checkNo": "7890123456",
    "_branchCode": null,
    "_accountNumber": "87654321",
    "_tcknVkn": "22966699784",
    "_bankCode": "0032",
    "_micrCode": null,
    "_checkAmount": "2300.50"
  }
]
```

## 🧪 Test Etme

Tek bir çek üzerinde test yapmak için:
```bash
python test_gemini_extraction.py
```

## 💡 Programatik Kullanım

Python kodunuzda doğrudan kullanmak için:

```python
from core import extract_cheque_information, ChequeProcessor

# Basit kullanım
results_file = extract_cheque_information(
    gemini_api_key="your_api_key",
    output_file="my_results.json"
)

# Gelişmiş kullanım
processor = ChequeProcessor("your_api_key")
results = processor.process_all_cheques()

# Tek tek işleme
from core import GeminiChequeExtractor

extractor = GeminiChequeExtractor("your_api_key")
info = extractor.extract_cheque_info("path/to/cheque.jpg")
```

## ⚠️ Önemli Notlar

1. **API Limitleri**: Gemini ücretsiz planında günlük istek limiti vardır
2. **Doğruluk**: AI çıkarımı %100 doğru olmayabilir, kritik bilgileri manuel olarak kontrol edin
3. **Desteklenen Formatlar**: JPG, JPEG, PNG, BMP, TIFF
4. **Görüntü Kalitesi**: Yüksek çözünürlüklü, net görüntüler daha iyi sonuç verir

## 🔧 Sorun Giderme

### API Anahtarı Hatası
```
❌ Error: GEMINI_API_KEY environment variable is not set!
```
**Çözüm**: API anahtarınızı environment variable olarak ayarlayın.

### İmport Hatası
```
❌ Import Error: No module named 'google.generativeai'
```
**Çözüm**: Gerekli paketleri yükleyin: `pip install -r requirements_gemini.txt`

### Boş Sonuçlar
Eğer tüm alanlar `null` dönüyorsa:
- Görüntü kalitesini kontrol edin
- Çekin Türkçe olduğundan emin olun
- API limitinizi kontrol edin

## 📞 Destek

Sorunlarınız için:
1. Önce bu kılavuzu kontrol edin
2. Test script'ini çalıştırın
3. Hata mesajlarını kaydedin
4. Geliştirici ekibine başvurun
