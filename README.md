# metro-simulation


# Proje Başlığı: 
Metro Simülasyonu

## Kısa Açıklama:
Bu projede bana verilmiş olan Metro Simülasyon kodunun eksik kısımlarını tamamladım ve yeni özellikler ekledim. Eklediğim özellikler şunlardır:
- Istasyonların engelli uyumlu olup olmaması.
- En uzun rota bulma.
- Rastgele gecikme ekledim ve bu gecikme ile beraber gerçek süreyi hesapladım.
- İstanbul ve İzmir şehirlerinin metro istasyonlarını ekledim.
- Yenı bır test seneryosu oluşturdum ve kullancının secımıne gore hesaplattım.

## Kullanılan Teknolojiler:
- heapq kütüphanesi (heapq, min-heap (küçükten büyüğe sıralı) yapısını kullanarak verileri verimli bir şekilde saklar ve işler. Veriler, öncelik değerine göre sıralanır. En düşük değerli öğe her zaman ilk sıradadır. Ekleme (heappush()) ve çıkarma (heappop()) işlemlerini O(log n) karmaşıklığıyla gerçekleştirir.)
- random kütüphanesi (rastgele sayı üretimi ve rastgele işlemler yapmak için kullanılan standart bir kütüphanedir. Bu kütüphane ile rastgele seçimler yapabilir, karışık listeler oluşturabilir veya belirli bir aralıktan rastgele sayılar üretebiliriz.)
- collections kütüphanesi (Bu kütüphane veri yapıları ile ilgili yardımcı fonksiyonları kullanmamızı sağlar. Bu projede de defaultdıct ve deque kullandım.)
- typing kütüphanesi (Bu kütüphaneden type hints import ediyoruz, bunlar kodumuzun daha anlaşılır ve güvenilir olmasını sağlıyor.)

## Kullandığım algoritmalar, nasıl çalıştıkları, neden kullandığım:
- En az hızlı rota için A* algoritması kullanıldı. A* algoritması, en kısa veya en hızlı yolu bulmak için kullanılan bir arama algoritmasıdır. Dijkstra'nın algoritması gibi çalışır, ancak bir öncelik sırası (priority queue(pq)) kullanarak hedefe olan tahmini maliyeti (a_yıldız) de hesaba katar. Bu sayede, daha kısa yolların öncelikli olarak seçilmesine yardımcı olur ve daha hızlı bir çözüm bulmayı sağlar.
- En az aktarmalı rota için BFS algoritması kullanıldı. BFS, bir graf üzerinde en kısa yolu bulmak için kullanılan bir arama algoritmasıdır. Başlangıç noktasından başlayarak, komşu düğümleri keşfeterek hedefe ulaşmaya çalışır. En kısa yolu bulmaya çalıştığımz için bu algoritmayı tercih ettik. Düğümler, FIFO yapısındaki bir kuyrukta saklanır. Her seferinde kuyruğun başındaki düğüm çıkarılır ve geçerli düğümün komşuları kuyruğa eklenir. En kısa yolu garanti eder fakat hedef düğüme ulaşmak için tüm düğümleri taramak zorunda kalabilir.
- En uzun yolu bulmak için DFS algoritması kullanıldı. DFS, bir graf üzerinde bir düğümün tüm komşularını keşfetmek için kullanılan bir arama algoritmasıdır. Başlangıç noktasından başlayarak, bir düğümün tüm komşularını keşfeterek hedefe ulaşmaya çalışır. En uzun yolu bulmaya çalıştığımz için bu algoritmayı tercih ettik.

## Örnek kullanım ve test sonuçları:
Kodumun test sonuçlarında ilk önce test senaryolarının cevaplarını alıyoruz, örnekteki gibi almıyoruz biraz daha değiştirdim rotalardan sonra alt satıra inmekte ve bütün istasyonların yanında engelli uyumluluğunu belirten sembolleri ekledim. Bizden vermemizi istediğiniz süreyi Normal seyahat süresi olarak ekledim onun da altında Tahmini gerçek süre var bu süre de rastgele oluşturduğumuz gecikme sürelerini de ekleyip veriyor. Ayrıca bunların üstünde Yolculuk ücreti ekledim bu ücret temel olarak 5Tl ve alan farkında gore 2.5TL artıcak şekilde ayarladım. Istedıgınız rotaların altında en uzun yolu buldugumuz bır kısım ekledım burda DSF algoritmasını kullanıp size a noktasından b noktasına en uzun sekilde nasıl gideriz bunun çıktısını veriyoruz. En sonda kendim 4. senaryo olarak kullanıcıdan ilk önce şehir seçtirtiyoruz sonrasında kullanıcıya şehir içerisinde istasyonların listesini veriyoruz ve başlangıç, son istasyon IDlerini alıyoruz. Bu idler üzerinden kodum rotaları önümüze getiriyor.


## Projeyi geliştirme fikrim:
Projeyi geliştiriken ilk öncelikle bizden istediğiniz kısımları tamamladım. Bunu yapabilmek için detaylıca A* algoritmasını araştırdım. Sonrasında geliştirme olarak aklıma ilk gelen şey rahatça diğer şehirlerin metrosunu da ekliyebilmek oldu bunu yaptıktan sonra Ankara dışında 2 büyükşehirin İstanbul ve İzmir şehirlerinin metro istasyonlarını ekledim. Daha sonrasında test seneryoları oluşturup kullanıcının istediği şehirleri seçmesini sağladım. Bu sayede kullanıcının istediği şehirleri seçerek en kısa yolu bulmasını sağladım. Nasıl geliştirebilirim diye düşünmeye devam ettiğimde aklıma istasyonlara değer vermek ve bu değerlerin en yüksek olduğu şekilde rota oluşturmak geldi, yaptım ama sonrasında beğenmedim ve onun yerine istasyonların engelli uyumlu olup olmamasını ekledim bunu random kütüphanesi ile şansa bağladım. Gecikmeler ile yeni bir süre algısı yarattım ve ayrıca metro kullanmanın ücreti olacağı için gittiğin kadar öde mantığıyla bir fiyatlandırma kodladım.

