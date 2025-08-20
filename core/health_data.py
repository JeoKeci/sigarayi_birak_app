# core/health_data.py

# Sigarayı bıraktıktan sonra ulaşılan sağlık hedefleri.
# Yapı: (Ulaşmak için gereken saat, "Açıklama metni")
# Veriler, işlenmesi kolay olması için artan saat sırasına göre dizilmiştir.

HEALTH_MILESTONES = [
    (8, "Kanınızdaki karbonmonoksit seviyesi normale döner, oksijen seviyesi artar."),
    (24, "Kalp krizi geçirme riskiniz azalmaya başlar."),
    (48, "Hasar görmüş sinir uçları onarılmaya başlar, tat ve koku alma duyularınız artar."),
    (72, "Akciğerlerinizdeki bronş tüpleri gevşer, nefes almanız kolaylaşır ve enerji seviyeniz yükselir."),
    (336, "Kan dolaşımınız iyileşir, yürüme ve egzersiz yapmak kolaylaşır. (2 Hafta)"),
    (720, "Akciğer fonksiyonlarınız %30'a kadar artar, öksürük ve nefes darlığı azalır. (1 Ay)"),
    (2160, "Akciğerleriniz kendini temizlemeye devam eder, enfeksiyon riski azalır. (3 Ay)"),
    (8760, "Koroner kalp hastalığı riskiniz sigara içen birine göre yarı yarıya azalır. (1 Yıl)"),
    (43800, "Felç geçirme riskiniz, sigara içmemiş birinin seviyesine iner. (5 Yıl)"),
    (87600, "Akciğer kanserinden ölme riskiniz sigara içen birine göre yarı yarıya azalır. (10 Yıl)"),
    (131400, "Koroner kalp hastalığı riskiniz, hiç sigara içmemiş birininkiyle aynı seviyeye gelir. (15 Yıl)"),
]