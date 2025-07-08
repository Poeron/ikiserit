# İkişerit - Adaptive Traffic Light Control System

Bu proje, SUMO (Simulation of Urban MObility) simülatörü kullanarak adaptif trafik ışığı kontrol sistemi geliştirmek için tasarlanmıştır. Sistem, gerçek zamanlı trafik yoğunluğu verilerini analiz ederek trafik ışıklarının zamanlamasını dinamik olarak optimize eder.

## 🚦 Proje Hakkında

Bu adaptif trafik ışığı kontrol sistemi, geleneksel sabit zamanlı trafik ışıklarından farklı olarak:

- **Gerçek zamanlı trafik yoğunluğu analizi** yapır
- **Dinamik faz değiştirme** ile trafik akışını optimize eder
- **Minimum ve maksimum yeşil ışık sürelerini** dikkate alır
- **Kavşak bazlı yoğunluk hesaplaması** ile karar verir

## 🏗️ Proje Yapısı

```
├── adaptive_tls.py          # Ana adaptif trafik ışığı kontrol script'i
├── network.net.xml          # SUMO ağ tanımı (yollar ve kavşaklar)
├── network.netecfg          # SUMO ağ yapılandırma dosyası
├── routes.rou.xml           # Araç rotaları ve trafik akış tanımları
├── sumo.sumocfg            # SUMO ana yapılandırma dosyası
├── trafficlight.tll.xml     # Trafik ışığı tanımları
└── README.md               # Bu dosya
```

## 📋 Önkoşullar

- **Python 3.7+**
- **SUMO 1.20+** (Eclipse SUMO simülatörü)
- **TraCI** (SUMO ile Python arasındaki iletişim için)

### SUMO Kurulumu

1. [SUMO'yu indirin](https://www.eclipse.org/sumo/downloads.php)
2. `SUMO_HOME` ortam değişkenini ayarlayın:
   ```bash
   # Windows PowerShell
   $env:SUMO_HOME = "C:\Path\To\Sumo"
   
   # Linux/Mac
   export SUMO_HOME="/path/to/sumo"
   ```

## 🚀 Kullanım

### Simülasyonu Başlatma

```bash
python adaptive_tls.py
```

### Proje Bileşenleri

#### 1. Adaptif Kontrol Algoritması (`adaptive_tls.py`)

- **Minimum yeşil süre**: 20 saniye
- **Maksimum yeşil süre**: 60 saniye
- **Sarı ışık süresi**: 3 saniye
- **Kavşak ID**: J8_joined

#### 2. Ağ Yapısı (`network.net.xml`)

Proje 4 ana kavşağı içerir:
- **J5** (Kuzey): E0 kenarından gelen trafik
- **J6** (Doğu): -E3 kenarından gelen trafik
- **J7** (Güney): -E2 kenarından gelen trafik
- **J8** (Batı): -E1 kenarından gelen trafik

#### 3. Trafik Fazları

```
Faz 0: "GGGGrrrrGGGGGGGGrrGGGGrr" - Kuzey-Güney yeşil
Faz 1: "yyGGrrrrGGyyyyGGrrGGyyrr" - Sarı geçiş
Faz 2: "rrGGGGGGGGrrrrGGGGGGrrGG" - Doğu-Batı yeşil
Faz 3: "rrGGyyyyGGrrrrGGyyGGrryy" - Sarı geçiş
```

#### 4. Araç Tipleri (`routes.rou.xml`)

- **Araba**: Hız 50 km/h, uzunluk 5m
- **Otobüs**: Hız 40 km/h, uzunluk 12m
- **Motosiklet**: Hız 55 km/h, uzunluk 2m
- **Kamyon**: Hız 30 km/h, uzunluk 15m

## 🧠 Algoritma Mantığı

### Karar Verme Kriterleri

1. **Maksimum süre kontrolü**: Yeşil ışık 60 saniyeyi geçerse faz değişir
2. **Yoğunluk analizi**: Bekleyen yöndeki trafik yoğunluğu, aktif yöndekinin 1.5 katından fazlaysa faz değişir
3. **Minimum süre garantisi**: Her yeşil faz en az 20 saniye sürer

### Yoğunluk Hesaplama

```python
# Her kavşak için araç yoğunluğu hesaplanır
density = total_vehicles / total_length
```

## 📊 Çıktı Örnekleri

```
J5 (North) density: 0.0250
J6 (East) density: 0.0180
J7 (South) density: 0.0320
J8 (West) density: 0.0290

Current green density: 0.0285, Waiting density: 0.0235
Switching traffic light phase because maximum green time reached.
Switched to EAST-WEST green
```

## 🔧 Konfigürasyon

### Parametreleri Değiştirme

`adaptive_tls.py` dosyasında aşağıdaki parametreler ayarlanabilir:

```python
MIN_GREEN_TIME = 20  # Minimum yeşil süre
MAX_GREEN_TIME = 60  # Maksimum yeşil süre
YELLOW_TIME = 3      # Sarı ışık süresi
JUNCTION_ID = "J8_joined"  # Kontrol edilen kavşak ID'si
```

## 🤝 Katkıda Bulunma

1. Bu repository'yi fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/YeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/YeniOzellik`)
5. Pull Request oluşturun

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 📞 İletişim

Proje hakkında sorularınız için GitHub Issues bölümünü kullanabilirsiniz.

## 🔗 Kaynaklar

- [SUMO Dokümantasyonu](https://www.eclipse.org/sumo/documentation.php)
- [TraCI Dokümantasyonu](https://sumo.dlr.de/docs/TraCI.html)
- [SUMO Tutorials](https://sumo.dlr.de/docs/Tutorials.html)
