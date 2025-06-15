import os

# Upload folder configuration
UPLOAD_FOLDER = 'uploads'

# Document categories
CATEGORY_FOLDERS = [
    'invoices', 'ids', 'cheque', 'signature_declaration',
    'residence_certificate', 'trade_registry_gazette',
    'driver_license', 'population_register', 'tax_plate',
    'contracts', 'kvkk_explicit_consent', 'digital_abf_commitment',
    'power_of_attorney', 'abf', 'cheque_customer_screening',
    'promissory_note', 'offset_and_payment_order',
    'unprocessed_return_payment_order', 'others', 'error_files',
    'factoring_agreement', 'activity_certificate', 'independent_audit_certificate'
]

# OCR categories and keywords
CATEGORIES = {
    "trade_registry_gazette": [
        'türkiye ticaret sicili gazetesi', 'ticaret sicili müdürlüğü'
    ],
    "digital_abf_commitment": [
        'dijital abf taahhütnamesi', 'taahhütte bulunan', 'tarafınızla akdetmiş olduğum', 'sms ile', 'sms'
    ],
    "kvkk_explicit_consent": [
        '6698 sayılı', 'kişisel verilerin korunması kanunu', 'açık rıza metni', 'veri sorumlusu', 'aydınlatma metni', 'rıza gösteriyorum'
    ],
    "factoring_agreement": [
        'faktoring hizmet sözleşmesi', 'alacakların devri', 'temlik', 'finansman hizmeti', 'faktör şirketi'
    ],
    "power_of_attorney": [
        'vekaletname', 'vekil tayin ettim', 'adıma işlem yapmaya yetkilidir', 'noter tasdikli vekaletname', 'işbu vekaletname ile'
    ],
    "signature_declaration": [
        'imza beyannamesi', 'imzaya yetkili kişi', 'ticaret sicil müdürlüğü', 'imza örneği'
    ],
    "abf": [
        'abf formu', 'abf başvuru', 'abf numarası', 'abf', 'alacak bildirimi formu'
    ],
    "ids": [
        't.c. kimlik no', 't.c. kimlik no.', 'nüfus cüzdanı', 'kimlik kartı', 'türkiye cumhuriyeti',
        'uyruğu', 'gender', 'nationality', 'identity card'
    ],
    "invoices": [
        'e-fatura', 'ettn', 'fatura no', 'fatura tarihi', 'fatura tipi', 'mal hizmet toplam tutarı', 'fatura',
        'invoice', 'ınvoıce', 'taşıma irsaliye', 'taşıma ırsaliye', 'müşteri v.d.', 'müşteri v.d.no.', 'irsaliye'
    ],
    "cheque": [
        'çek', 'keşideci', 'keşide yeri', 'çek seri no', 'çak', 'çak no', 'tacir', 'basım tarihi', 'keşide', 'bu çek', 'çek karşılığında',
        'bu çek karşılığında', 'findeks', 'çok seri no', 'çok sori no', 'mersis no', 'morsis no'
    ],
    "promissory_note": [
        'senet', 'emre yazılı senet', 'borçlunun adı', 'ödenecek meblağ', 'vade tarihi', 'düzenlenme yeri'
    ],
    "contracts": [
        'taraflar arasında akdedilmiştir', 'işbu sözleşme', 'sözleşmenin konusu', 'hak ve yükümlülükler', 'tarafların mutabakatı', 'kefalet',
        'faktoring sözleşmesi', 'sözleşmesi'
    ],
    "residence_certificate": [
        'yerleşim yeri belgesi', 'yerleşim yeri', 'ikametgah belgesi', 'adres kayıt sistemi', 'nüfus ve vatandaşlık işleri genel müdürlüğü'
    ],
    "driver_license": [
        'sürücü belgesi', 'driving licence', 'veriliş tarihi', 'sınıf', 'ehliyet no'
    ],
    "population_register": [
        'nüfus kayıt örneği', 'nüfus kayıt', 'nüfus kayit örneği', 'aile sıra no', 'cilt no', 'mahallesi', 'nüfus müdürlüğü'
    ],
    "tax_plate": [
        'vergi levhası', 'vergi kimlik no', 'vergı levhası', 'faaliyet kodu', 'gelir idaresi', 'beyan edilen matrah',
        'vergi levhası', 'gelir idaresi', 'levhası', 'beyan olunan matrah', 'matrah', 'vergi türü', 'vergi kimlik', 'tahakkuk eden vergi',
        'intvd.gib.gov.tr'
    ],
    "offset_and_payment_order": [
        'ödeme emri', 'mahsup talebi', 'vergi dairesi müdürlüğü', '6183 sayılı kanun'
    ],
    "unprocessed_return_payment_order": [
        'işlenmemiş iade', 'ödenmemiş ödeme emri', 'vergi iadesi talebi', 'beyanname bilgileri'
    ],
    "activity_certificate": [
        'faaliyet sicili', 'ticaret sicil tasdiknamesi', 'ticaret sicil', 'faaliyet belgesi', 'commercial activity',
        'nace kodu', 'nace code', 'faaliyet bilgileri', 'faaliyet kodu', 'sicil kayıt sureti', 'ticaret', 'sicil kayıt', 'sicil'
    ],
    "independent_audit_certificate": [
        'bağımsız denetime tabi', 'denetime tabi', 'bağımsız denetim yükümlülüğü', 'bağımsız denetim', 'smmm', 'ymm', 'mali müşavirlerce'
    ]
}

def setup_directories():
    """Create all necessary directories for the project."""
    for folder in CATEGORY_FOLDERS:
        os.makedirs(os.path.join(UPLOAD_FOLDER, folder), exist_ok=True)
