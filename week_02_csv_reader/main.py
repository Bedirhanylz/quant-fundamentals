from finans_araclari import gunluk_getiri, hareketli_ortalama, sinyal_uret
from csv_okuyucu import tarih_ve_fiyat_oku, close_fiyatlarini_oku, csv_dict_oku

def main(): 
    fiyatlar= close_fiyatlarini_oku('veri.csv')
    tarih_ve_fiyatlar = tarih_ve_fiyat_oku('veri.csv')

    getiriler = gunluk_getiri(fiyatlar)
    ortalamalar = hareketli_ortalama(fiyatlar,3)
    sinyaller = sinyal_uret(fiyatlar, 3, 5)
    print('Tarih ve fiyatlar')
    print(tarih_ve_fiyatlar)
    print('Close fiyatları')
    print(fiyatlar)
    print('günlük getiriler')
    print(getiriler)
    print("3 günlük hareketli ortalama:")
    print(ortalamalar)

    print("Sinyaller:")
    print(sinyaller)

if __name__ == '__main__': 
    main()