fiyatlar =  [
    312.51, 310.85, 308.33, 308.82, 304.99, 302.25, 298.97, 297.84, 300.23, 298.21, 298.87, 294.8, 292.68, 293.32, 287.44, 287.51, 284.18, 276.83, 280.14, 271.35, 270.17, 270.71, 267.61, 271.06, 273.43, 273.17, 266.17, 273.05, 270.23, 263.4
    ]
fiyatlar.reverse()

def gunluk_getiri(liste): 
    getiriler = []
    for i in range(1 , len(liste)): 
        getiri = (liste[i] - liste[i-1]) / liste[i-1]
        getiriler.append(getiri)
    return(getiriler)

def hareketli_ortalama_5(liste, pencere = 5):
    sma_5_list = []
    for i in range(pencere - 1, len(liste)): 
        dilim = liste[i + 1 - pencere : i + 1]
        ortalama = sum(dilim) / 5
        sma_5_list.append(ortalama)
        i = i + 1 
    return sma_5_list
        
def hareketli_ortalama_20(liste, pencere = 20):
    sma_20_list = []
    for i in range(pencere - 1, len(liste)): 
        dilim = liste[i + 1 - pencere : i + 1]
        ortalama = sum(dilim) / 20
        sma_20_list.append(ortalama)
    return sma_20_list

def sinyal_uret(sma5, sma20):
    sinyaller = []
    for i in range(1, len(sma20)):
        if sma5[i-1] < sma20[i-1] and sma5[i] > sma20[i]:
            sinyaller.append('AL')
        elif sma5[i-1] > sma20[i-1] and sma5[i] < sma20[i]:
            sinyaller.append('SAT')
        else:
            sinyaller.append('TUT')
    return sinyaller
 
HISSE = 'AAPL'

# listeleri alalım 
getiriler = gunluk_getiri(fiyatlar)
sma5 = hareketli_ortalama_5(fiyatlar)
sma20 = hareketli_ortalama_20(fiyatlar)

# sinyal için ema5 ile ema20 yi hizalayalım
sma5_for_signal = sma5[len(sma5) - len(sma20) :]
sinyaller = sinyal_uret(sma5_for_signal , sma20)


#tüm listeleri sinyallerin sayısına göre hizalayalım 
n = len(sinyaller)
fiyatlar_hiz = fiyatlar[-n:]
sma5_hiz = sma5[-n:]
sma20_hiz = sma20[-n:]

print(f"=== Hisse Analizi: {HISSE} ===")
print(f"{'Gün':<5} | {'Fiyat':<8} | {'MA5':<8} | {'MA20':<8} | Sinyal")
print("-" * 50)

baslangic_gunu = len(fiyatlar) - n

for i in range(n): 
    gun = baslangic_gunu + i
    print(
        f"{gun:<5} | "
        f"{fiyatlar_hiz[i]:<8.2f} | "
        f"{sma5_hiz[i]:<8.2f} | "
        f"{sma20_hiz[i]:<8.2f} | "
        f"{sinyaller[i]}"
    )
