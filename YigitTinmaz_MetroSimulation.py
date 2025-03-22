from collections import defaultdict, deque
import heapq
import random
from typing import Dict, List, Set, Tuple, Optional

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []  # (istasyon, süre) tuple'ları
        self.engelli_erisimi = False  # Engelli erişimi var mı?
        self.gecikme = 0  # Anlık gecikme süresi (dakika)
        self.alan = 1  # İstasyonun bulunduğu bölge

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        self.komsular.append((istasyon, sure))

class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)
        self.temel_ucret = 5.0  # Temel bilet ücreti
        self.alan_ucret = 2.5  # Alan başına ek ücret
        self.max_gecikme = 15  # Maksimum gecikme süresi (dakika)

    def istasyon_durumu_guncelle(self, istasyon_id: str, engelli_erisimi: bool = None, alan: int = None) -> None:
        # İstasyon durumunu günceller (engelli erişimi ve alan bilgisi)
        if istasyon_id in self.istasyonlar:
            istasyon = self.istasyonlar[istasyon_id]
            if engelli_erisimi is not None:
                istasyon.engelli_erisimi = engelli_erisimi
            if alan is not None:
                istasyon.alan = alan

    def rastgele_gecikme_uret(self) -> None:
        # Tüm istasyonlar için rastgele gecikme süreleri oluşturur
        import random
        for istasyon in self.istasyonlar.values():
            # %20 ihtimalle gecikme oluştur
            if random.random() < 0.2:
                istasyon.gecikme = random.randint(1, self.max_gecikme)
            else:
                istasyon.gecikme = 0

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        if idx not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)
    
    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        ziyaret_edildi = {baslangic}
        
        kuyruk = deque([(baslangic, [baslangic])])
        
        while kuyruk:
            current, path = kuyruk.popleft()
            
            if current == hedef:
                return path
            
            for komsu, _ in current.komsular:
                if komsu not in ziyaret_edildi:
                    ziyaret_edildi.add(komsu)
                    kuyruk.append((komsu, path + [komsu]))
        
        return None

    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        ziyaret_edildi = set()
        
        def a_yıldız(istasyon: Istasyon) -> int:
            # Hat değişimi gerekiyorsa kafadan 5 eklettiriyoruz geldıysek zaten gelmısızdır.
            if istasyon.hat == hedef.hat:
                return 0
            else:
                return 5 
        
        # A* algoritması için öncelik kuyruğu: (f_score, id, istasyon, path, g_score)
        # f_score = g_score (gerçek maliyet) + h_score (tahmini maliyet)
        pq = [(0 + a_yıldız(baslangic), id(baslangic), baslangic, [baslangic], 0)]
        
        while pq:
            _, _, current, path, g_score = heapq.heappop(pq)
            
            if current == hedef:
                return path, g_score
            
            if current in ziyaret_edildi:
                continue
                
            ziyaret_edildi.add(current)
            
            for komsu, sure in current.komsular:
                if komsu not in ziyaret_edildi:
                    yeni_g_score = g_score + sure
                    f_score = yeni_g_score + a_yıldız(komsu)
                    heapq.heappush(pq, (f_score, id(komsu), komsu, path + [komsu], yeni_g_score))
        
        return None

    def ucret_hesapla(self, baslangic_id: str, hedef_id: str) -> float:
        # İki istasyon arasındaki seyahat ücretini hesaplar.
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return 0.0
        
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        alan_farki = abs(hedef.alan - baslangic.alan)
        
        return self.temel_ucret + (alan_farki * self.alan_ucret)
    
    def gercek_zamanli_sure(self, rota: List[Istasyon]) -> int:
        # Rota üzerindeki toplam süreyi gecikmeleri de hesaba katarak hesaplar.
        if not rota or len(rota) < 2:
            return 0
        
        toplam_sure = 0
        for i in range(len(rota) - 1):
            for komsu, sure in rota[i].komsular:
                if komsu == rota[i + 1]:
                    toplam_sure += sure + rota[i].gecikme + rota[i + 1].gecikme
                    break
        return toplam_sure



    def en_uzun_yol_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        
        def dfs(current: Istasyon, hedef: Istasyon, path: List[Istasyon], ziyaret_edildi: Set[Istasyon]) -> Optional[List[Istasyon]]:
            if current == hedef:
                return path[:]
            
            en_uzun_yol = None
            
            for komsu, _ in current.komsular:
                if komsu not in ziyaret_edildi:
                    ziyaret_edildi.add(komsu)
                    yeni_yol = dfs(komsu, hedef, path + [komsu], ziyaret_edildi)
                    ziyaret_edildi.remove(komsu)
                    
                    if yeni_yol and (not en_uzun_yol or len(yeni_yol) > len(en_uzun_yol)):
                        en_uzun_yol = yeni_yol
            
            return en_uzun_yol
        
        ziyaret_edildi = {baslangic}
        path = dfs(baslangic, hedef, [baslangic], ziyaret_edildi)
        
        if path:
            toplam_sure = 0
            for i in range(len(path) - 1):
                for komsu, sure in path[i].komsular:
                    if komsu == path[i + 1]:
                        toplam_sure += sure
                        break
            return path, toplam_sure
        
        return None

if __name__ == "__main__":
    # Şehir metro ağları
    sehir_metro = {
        "Ankara": MetroAgi(),
        "Istanbul": MetroAgi(),
        "Izmir": MetroAgi()
    }
    
    # Ankara Metro Ağı
    ankara = sehir_metro["Ankara"]
    
    # Ankara İstasyonları ekleme
    # Kırmızı Hat
    ankara.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    ankara.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    ankara.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    ankara.istasyon_ekle("K4", "OSB", "Kırmızı Hat")
    
    # Mavi Hat
    ankara.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    ankara.istasyon_ekle("M2", "Kızılay", "Mavi Hat")  # Aktarma noktası
    ankara.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    ankara.istasyon_ekle("M4", "Gar", "Mavi Hat")
    
    # Turuncu Hat
    ankara.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    ankara.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  # Aktarma noktası
    ankara.istasyon_ekle("T3", "Gar", "Turuncu Hat")  # Aktarma noktası
    ankara.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")
    
    # Bağlantılar ekleme
    # Kırmızı Hat bağlantıları
    ankara.baglanti_ekle("K1", "K2", 4)  # Kızılay -> Ulus
    ankara.baglanti_ekle("K2", "K3", 6)  # Ulus -> Demetevler
    ankara.baglanti_ekle("K3", "K4", 8)  # Demetevler -> OSB
    
    # Mavi Hat bağlantıları
    ankara.baglanti_ekle("M1", "M2", 5)  # AŞTİ -> Kızılay
    ankara.baglanti_ekle("M2", "M3", 3)  # Kızılay -> Sıhhiye
    ankara.baglanti_ekle("M3", "M4", 4)  # Sıhhiye -> Gar
    
    # Turuncu Hat bağlantıları
    ankara.baglanti_ekle("T1", "T2", 7)  # Batıkent -> Demetevler
    ankara.baglanti_ekle("T2", "T3", 9)  # Demetevler -> Gar
    ankara.baglanti_ekle("T3", "T4", 5)  # Gar -> Keçiören
    
    # Hat aktarma bağlantıları 
    ankara.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma
    ankara.baglanti_ekle("K3", "T2", 3)  # Demetevler aktarma
    ankara.baglanti_ekle("M4", "T3", 2)  # Gar aktarma


    
    # Istanbul Metro Ağı
    istanbul = sehir_metro["Istanbul"]
    # M1A Hattı (Yenikapi-Atatürk Havalimanı)
    istanbul.istasyon_ekle("I1", "Yenikapi", "M1A")
    istanbul.istasyon_ekle("I2", "Aksaray", "M1A")
    istanbul.istasyon_ekle("I3", "Atatürk Havalimanı", "M1A")
    
    # M2 Hattı (Taksim-Hacıosman)
    istanbul.istasyon_ekle("I4", "Taksim", "M2")
    istanbul.istasyon_ekle("I5", "Şişhane", "M2")
    istanbul.istasyon_ekle("I6", "Hacıosman", "M2")
    
    # M4 Hattı (Kadıköy-Tavşantepe)
    istanbul.istasyon_ekle("I7", "Kadıköy", "M4")
    istanbul.istasyon_ekle("I8", "Kartal", "M4")
    istanbul.istasyon_ekle("I9", "Tavşantepe", "M4")
    
    # Istanbul Bağlantıları
    istanbul.baglanti_ekle("I1", "I2", 5)
    istanbul.baglanti_ekle("I2", "I3", 8)
    istanbul.baglanti_ekle("I4", "I5", 4)
    istanbul.baglanti_ekle("I5", "I6", 7)
    istanbul.baglanti_ekle("I7", "I8", 6)
    istanbul.baglanti_ekle("I8", "I9", 5)
    istanbul.baglanti_ekle("I1", "I5", 3)  # Yenikapi-Şişhane aktarma
    istanbul.baglanti_ekle("I5", "I7", 4)  # Şişhane-Kadıköy aktarma 
    

    
    # İzmir Metro Ağı
    izmir = sehir_metro["Izmir"]
    # F1 Hattı (Fahrettin Altay-Evka 3)
    izmir.istasyon_ekle("Z1", "Fahrettin Altay", "F1")
    izmir.istasyon_ekle("Z2", "Üçyol", "F1")
    izmir.istasyon_ekle("Z3", "Konak", "F1")
    izmir.istasyon_ekle("Z4", "Halkapınar", "F1")
    izmir.istasyon_ekle("Z5", "Evka 3", "F1")
    
    # K1 Hattı (Karşıyaka-Mavişehir)
    izmir.istasyon_ekle("Z6", "Karşıyaka", "K1")
    izmir.istasyon_ekle("Z7", "Mavişehir", "K1")
    
    # İzmir Bağlantıları
    izmir.baglanti_ekle("Z1", "Z2", 4)
    izmir.baglanti_ekle("Z2", "Z3", 5)
    izmir.baglanti_ekle("Z3", "Z4", 6)
    izmir.baglanti_ekle("Z4", "Z5", 7)
    izmir.baglanti_ekle("Z6", "Z7", 5)
    izmir.baglanti_ekle("Z4", "Z6", 3)  # Halkapınar-Karşıyaka aktarma
    

    
    def goster_istasyonlar(metro_agi):
        print("\nMevcut İstasyonlar:")
        for idx, istasyon in metro_agi.istasyonlar.items():
            print(f"{idx}: {istasyon.ad} ({istasyon.hat})")

    def kullanici_rota_hesapla(metro_agi, baslangic_id, hedef_id):
        print(f"Rotalar {metro_agi.istasyonlar[baslangic_id].ad}'dan {metro_agi.istasyonlar[hedef_id].ad}'a:")
        # Rastgele gecikmeleri oluştur
        metro_agi.rastgele_gecikme_uret()
        # Engelli erişimi durumunu rastgele ayarla
        for istasyon in metro_agi.istasyonlar.values():
            metro_agi.istasyon_durumu_guncelle(istasyon.idx, engelli_erisimi=random.choice([True, False]))
        # Ücret hesapla
        ucret = metro_agi.ucret_hesapla(baslangic_id, hedef_id)
        print(f"\nYolculuk ücreti: {ucret:.2f} TL")
        
        # En az aktarmalı rota
        rota = metro_agi.en_az_aktarma_bul(baslangic_id, hedef_id)
        if rota:
            gercek_sure = metro_agi.gercek_zamanli_sure(rota)
            print(f"\nEn az aktarmalı rota ({len(rota)} istasyon):\nGüzergah: " + " -> ".join(f"{i.ad} {'♿' if i.engelli_erisimi else '❌'}" for i in rota))
            print(f"Tahmini gerçek seyahat süresi: {gercek_sure} dakika")
        else:
            print("\nBurdan buraya aktarma bulunmadigi icin gidemezsiniz")
        
        # En hızlı rota
        sonuc = metro_agi.en_hizli_rota_bul(baslangic_id, hedef_id)
        if sonuc:
            rota, sure = sonuc
            gercek_sure = metro_agi.gercek_zamanli_sure(rota)
            print(f"\nEn hızlı rota ({len(rota)} istasyon):\nGüzergah: " + " -> ".join(f"{i.ad} {'♿' if i.engelli_erisimi else '❌'}" for i in rota))
            print(f"Normal seyahat süresi: {sure} dakika")
            print(f"Tahmini gerçek seyahat süresi: {gercek_sure} dakika")
        
        # En uzun yol
        uzun = metro_agi.en_uzun_yol_bul(baslangic_id, hedef_id)
        if uzun:
            rota, sure = uzun
            gercek_sure = metro_agi.gercek_zamanli_sure(rota)
            print(f"\n**En uzun yol ({len(rota)} istasyon):\nGüzergah: " + " -> ".join(f"{i.ad} {'♿' if i.engelli_erisimi else '❌'}" for i in rota))
            print(f"Normal seyahat süresi: {sure} dakika")
            print(f"Tahmini gerçek seyahat süresi: {gercek_sure} dakika")
        


    # Test senaryoları
    print("\n=== Test Senaryoları ===")
    
    # Ankara senaryoları
    ankara = sehir_metro["Ankara"]
    print("\nAnkara Metro Senaryoları:")
    
    # Alanları ayarla sadece ankara
    for istasyon in ankara.istasyonlar.values():
        ankara.istasyon_durumu_guncelle(istasyon.idx, alan=random.randint(1, 4))
    
    # Senaryo 1: AŞTİ'den OSB'ye
    print("\n1. AŞTİ'den OSB'ye:")
    kullanici_rota_hesapla(ankara, "M1", "K4")
    
    # Senaryo 2: Batıkent'ten Keçiören'e
    print("\n2. Batıkent'ten Keçiören'e:")
    kullanici_rota_hesapla(ankara, "T1", "T4")
    
    # Senaryo 3: Keçiören'den AŞTİ'ye
    print("\n3. Keçiören'den AŞTİ'ye:")
    kullanici_rota_hesapla(ankara, "T4", "M1")
    
    # Kullanıcı Seçimli Senaryo
    print("\n4. Kullanıcı Seçimli Rota:")
    print("\nŞehir Seçiniz:")
    print("1. Ankara")
    print("2. Istanbul")
    print("3. Izmir")
    
    sehir_secim = input("Şehir numarasını giriniz (1-3): ")
    sehir_map = {"1": "Ankara", "2": "Istanbul", "3": "Izmir"}
    
    if sehir_secim in sehir_map:
        secilen_sehir = sehir_map[sehir_secim]
        metro_agi = sehir_metro[secilen_sehir]
        
        # Alanları ayarla
        for istasyon in metro_agi.istasyonlar.values():
            metro_agi.istasyon_durumu_guncelle(istasyon.idx, alan=random.randint(1, 4))
        
        print(f"\n{secilen_sehir} Metro Ağı seçildi.")
        goster_istasyonlar(metro_agi)
        
        baslangic_id = input("\nBaşlangıç istasyonu ID'sini giriniz: ").upper()
        hedef_id = input("Hedef istasyonu ID'sini giriniz: ").upper()
        
        if baslangic_id in metro_agi.istasyonlar and hedef_id in metro_agi.istasyonlar:
            kullanici_rota_hesapla(metro_agi, baslangic_id, hedef_id)
        else:
            print("\nGeçersiz istasyon ID'leri girdiniz!")
    else:
        print("\nGeçersiz şehir seçimi!")