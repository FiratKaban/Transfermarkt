
XXX !!! ONCE TRANSFERMARKT.PY NIN DUZGUN CALISTIGINDAN EMIN OLUN !!! XXX
ARALARA PRINT EKLEYIP CIKARARAK DEBUG YAPABILIRSIN

TODO: DEGISKENLERIN DB'DE KARSILIGI OLMALI
      BUNUN ICIN LUCIDCHART VB CROWS FOOT NOTASYONU VB BI EXCEL DE OLABIIR
      HAZIRLARSAN, HAZIR VERIYE GORE DB YAPISINI GUNCELLEYEBILIRIZ

      DB'ye ekleme fonsiyon ornekleri gosterecegim. AWS postgresql kullanacagiz.
      orneklere gore tum degiskenlerin DB'ye yazilmasi kismi sende.

TODO: Bu yapi daha sonra dictinary olarak degistirilebilir. Yonetmesi daha kolay olur

XXX: bu formatta biz bir ligin sezonlarini almak yerine
XXX: bir ligdeki ilk sezonun baslangic yilini aliyoruz. orn: 1928
XXX: bu yuzden bundan sonraki fonksiyona try catch bloklari ekleyerek
XXX: hata aldigimizda ilgili ligin o sezon yilinda aktif olmadigini anlayacagiz
          
XXX: for each link in links list get all team data
     get all team data from league years using 'links' list            

TODO: XXX: FIRAT: yukaridaki if else blocklari try except ile degistirilmeli.
 sample of try catch blocks

        
XXX: for each link in links list get all team data
     get all team data from league years using 'links' list.
          
XXX: TEAMS.PY EKLENECEK

TODO: Class mantigi ve veritabani baglantisi icin kod revize edilecek.

XXX: end of the project: SERVICE SCRIPT
python uygulamasinin sunucuda surekli calismasi icin 
ve surekli calisan uygulamanin monitor edilebilmesi icin
cron job kullanilabilir. fakat uygulanabilirlik ve monitoring acisindan
degerlendirdiginde systemctl'de calisacak olan service scripti daha mantikli.
systemctl example link: https://www.digitalocean.com/community/tutorials/how-to-use-systemctl-to-manage-systemd-services-and-units
    
XXX: end of the project: ip reputation control & ip changer
how to check the string is string or integer
https://stackoverflow.com/questions/1265665/how-can-i-check-if-a-string-represents-an-int-without-using-try-except
