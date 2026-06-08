class Hisse: 
    def __init__(self, ticker, fiyatlar):
        self.ticker = ticker
        self.fiyatlar = fiyatlar

    def gunluk_getiri(self):
        gunluk_getiriler = []

        for i in range(1, len(self.fiyatlar)):
            getiri = (self.fiyatlar[i] - self.fiyatlar[i-1]) / self.fiyatlar[i-1]
            gunluk_getiriler.append(getiri)
        return gunluk_getiriler
    
    def hareketli_ortalama(self, pencere= 3): 
        ortalamalar = []

        for i in range(len(self.fiyatlar)): 
            if i + 1 < pencere: 
                ortalamalar.append(None)
            else: 
                dilim = self.fiyatlar[i + 1 - pencere:i + 1]
                ortalama = sum(dilim) / len(dilim)
                ortalamalar.append(ortalama)
        
        return ortalamalar
    
    def sinyal_uret(self, kisa_pencere = 3, uzun_pencere = 5): 
        sinyaller = []
        kisa_ortalama = self.hareketli_ortalama(kisa_pencere)
        uzun_ortalama = self.hareketli_ortalama(uzun_pencere)

        for i in range(len(self.fiyatlar)): 
            if kisa_ortalama[i] is None or uzun_ortalama[i] is None: 
                sinyaller.append(None)
            elif kisa_ortalama[i] < uzun_ortalama[i]:
                sinyaller.append('SAT')
            elif kisa_ortalama[i] > uzun_ortalama[i]:
                sinyaller.append('AL')
            else: 
                sinyaller.append('BEKLE')
        
        return sinyaller

aapl = Hisse("AAPL", [100, 102, 101, 105, 108, 106, 105, 108, 110])

x = aapl.sinyal_uret()
print(x)

