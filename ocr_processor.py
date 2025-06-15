import pytesseract
from PIL import Image
import cv2
import os
import re
from datetime import datetime
from pdf2image import convert_from_path

# Kategori ve anahtar kelimeler
categories = {
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
        'taraflar arasında akdedilmiştir', 'işbu sözleşme', 'sözleşmenin konusu', 'hak ve yükümlülükler', 'tarafların mutabakatı' , 'kefalet',
          'faktoring sözleşmesi', 'sözleşmesi'
    ],
    "residence_certificate": [
        'yerleşim yeri belgesi', 'yerleşim yeri','ikametgah belgesi', 'adres kayıt sistemi', 'nüfus ve vatandaşlık işleri genel müdürlüğü'
    ],
    "driver_license": [
        'sürücü belgesi', 'driving licence', 'veriliş tarihi', 'sınıf', 'ehliyet no'
    ],
    "population_register": [
        'nüfus kayıt örneği', 'nüfus kayıt', 'nüfus kayit örneği', 'aile sıra no', 'cilt no', 'mahallesi', 'nüfus müdürlüğü'
    ],
    "tax_plate": [
        'vergi levhası', 'vergi kimlik no', 'vergı levhası', 'faaliyet kodu', 'gelir idaresi', 'beyan edilen matrah'
    ],
    "offset_and_payment_order": [
        'ödeme emri', 'mahsup talebi', 'vergi dairesi müdürlüğü', '6183 sayılı kanun'
    ],
    "unprocessed_return_payment_order": [
        'işlenmemiş iade', 'ödenmemiş ödeme emri', 'vergi iadesi talebi', 'beyanname bilgileri'
    ],
    "vergi_levhası":[
        'vergi levhası', 'gelir idaresi', 'levhası', 'beyan olunan matrah', 'matrah', 'vergi türü', 'vergi kimlik', 'tahakkuk eden vergi',
        'intvd.gib.gov.tr'
    ],
    "faaliyet_belgesi":[
        'faaliyet sicili', 'ticaret sicil tasdiknamesi', 'ticaret sicil', 'faaliyet belgesi', 'commercial activity',
          'nace kodu', 'nace code', 'faaliyet bilgileri', 'faaliyet kodu', 'sicil kayıt sureti', 'ticaret', 'sicil kayıt', 'sicil'
    ],
    "bagımsız_denetim_belgesi":[
        'bağımsız denetime tabi', 'denetime tabi', 'bağımsız denetim yükümlülüğü', 'bağımsız denetim' , 'smmm', 'ymm', 'mali müşavirlerce'
    ]
}

#Dosya döndürme
def rotate_image(image_cv2, angle):
    if angle == 0:
        return image_cv2
    return cv2.rotate(image_cv2, {
        90: cv2.ROTATE_90_CLOCKWISE,
        180: cv2.ROTATE_180,
        270: cv2.ROTATE_90_COUNTERCLOCKWISE
    }[angle])

def ocr_text_from_image(img_cv2):
    config = r'--oem 3 --psm 6'
    pil_img = Image.fromarray(cv2.cvtColor(img_cv2, cv2.COLOR_BGR2RGB))
    return pytesseract.image_to_string(pil_img, config=config, lang='tur').lower()

def classify_text(text):
    for cat, keywords in categories.items():
        if any(word in text for word in keywords):
            return cat
    return 'others'

# TC doğrulama
def is_valid_tc(tc: str) -> bool:
    if not re.fullmatch(r'\d{11}', tc):
        return False
    digits = list(map(int, tc))
    if digits[0] == 0:
        return False
    if sum(digits[:10]) % 10 != digits[10]:
        return False
    if ((sum(digits[0:10:2]) * 7) - sum(digits[1:9:2])) % 10 != digits[9]:
        return False
    return True

def extract_tc_from_text(text: str) -> str:
    matches = re.findall(r'\b\d{11}\b', text)
    for match in matches:
        if is_valid_tc(match):
            return match
    return None

def is_valid_vkn(vkn):
    if not (vkn.isdigit() and len(vkn) == 10):
        return False

    digits = [int(d) for d in vkn]
    transformed = []

    for i in range(9):
        tmp = (digits[i] + (9 - i)) % 10
        tmp = 10 if tmp == 0 else tmp
        transformed.append(tmp)

    total = 0
    for i in range(9):
        power = 2 ** (9 - i)
        total += (transformed[i] * power) % 9

    check_digit = (10 - (total % 10)) % 10
    return digits[9] == check_digit


def extract_vkn_from_text(text: str) -> str:
    matches = re.findall(r'\b\d{10}\b', text)
    for match in matches:
        if is_valid_vkn(match):
            return match
    return None

def generate_unique_filename(code: str, folder: str, ext: str) -> str:
    date_str = datetime.now().strftime("%d%m%Y")
    base_name = f"{code}_{date_str}"
    filename = f"{base_name}.{ext}"
    counter = 1
    while os.path.exists(os.path.join(folder, filename)):
        filename = f"{base_name}({counter}).{ext}"
        counter += 1
    return filename

def classify_document(file_path, return_id=False):
    _, ext = os.path.splitext(file_path)

    if ext.lower() == ".pdf":
        pages = convert_from_path(file_path, dpi=300)
        pil_image = pages[0]
        temp_path = "temp_image.jpg"
        pil_image.save(temp_path)
        img = cv2.imread(temp_path)
        os.remove(temp_path)
    else:
        img = cv2.imread(file_path)

    if img is None:
        raise ValueError("Görsel yüklenemedi")

    tc_found, vkn_found = None, None

    for angle in [0, 90, 180, 270]:
        rotated = rotate_image(img, angle)
        try:
            text = ocr_text_from_image(rotated)
            tc_found = extract_tc_from_text(text)
            if not tc_found:
                vkn_found = extract_vkn_from_text(text)
            category = classify_text(text)
            if category != 'others':
                return (category, tc_found or vkn_found) if return_id else category
        except Exception:
            continue

    print("İlk OCR başarısız, görsel büyütülerek tekrar deneniyor...")
    upscale_img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    for angle in [0, 90, 180, 270]:
        rotated = rotate_image(upscale_img, angle)
        try:
            text = ocr_text_from_image(rotated)
            if not tc_found:
                tc_found = extract_tc_from_text(text)
            if not tc_found and not vkn_found:
                vkn_found = extract_vkn_from_text(text)
            category = classify_text(text)
            if category != 'others':
                print("Başarı: büyütülmüş görsel ile sınıflandırıldı.")
                return (category, tc_found or vkn_found) if return_id else category
        except Exception:
            continue

    return ('others', tc_found or vkn_found) if return_id else 'others'