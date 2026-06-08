import csv

def csv_dict_oku(dosya_yolu): 
    satirlar = []
    with open(dosya_yolu, 'r', encoding='utf-8') as dosya:
        okuyucu = csv.DictReader(dosya)

        for satir in okuyucu: 
            satirlar.append(satir)
    return satirlar


def close_fiyatlarini_oku(dosya_yolu): 
    close_fiyatlari= []

    with open(dosya_yolu, 'r', encoding='utf-8') as dosya: 
        okuyucu = csv.DictReader(dosya)

        for satir in okuyucu: 
            close_fiyat = float(satir['Close'])
            close_fiyatlari.append(close_fiyat)
    
    return close_fiyatlari

def tarih_ve_fiyat_oku(dosya_yolu): 
    tarih_ve_fiyatlar = []

    with open(dosya_yolu, 'r', encoding='utf-8') as dosya: 
        okuyucu = csv.DictReader(dosya)

        for satir in okuyucu: 
            close_fiyat = float(satir['Close'])
            tarih = satir['Date']
            tarih_ve_fiyatlar.append((tarih, close_fiyat))
    
    return tarih_ve_fiyatlar