Öncelikle, programın geliştirilmesi için kullanılan işletim sistemi sanal makine üzerinde oluşturulan, Linux tabanlı Debian işletim sistemidir. Bunun yanında derleyici olarak Visual Studio Code tercih edilmiştir. Projede belirlenen dil olarak Python kullanılmıştır. Sürüm olarak Python 3.8.2 tercih edilmiştir. Proje içeriğinde login, upload/download, listeleme vb. temel işlemlerin yapılabildiği bir program istenmiştir. Bu programın işlemlerinin sağlanması FTP adresi olarak Debian tarafından sunulan ftp.debian.org adresi kullanılmış ve testler bu server üzerinden gerçekleştirilmiştir. Adres içeriği Şekil 1.1’ de gösterildiği gibidir. 

 ![](https://user-images.githubusercontent.com/46966075/86835982-8adb8300-c0a5-11ea-99ee-f77e40537093.png)
- Şekil 1.1: Kullanılan FTP adresi

Program oluşturulurken bu FTP adresi ile bağlandı sağlanmış ve adres üzerinden işlemler gerçekleştirilmiştir. Gerekli program, işletim sistemi ve kütüphanelerin sağlanamaması gibi bir sorun ortaya çıktığında ortaya çıkan hatalar programın başka bilgisayarda işleyişini engelleye bilir. Bu nedenle programın çalıştırılması ve kodların işleyişi ayrıntılı bir şekilde anlatılacaktır.
### 1.	Program
Bu kısımda programın çalışma şekli ve kodlar ayrıntılı bir şekilde anlatılacaktır. Programı daha iyi anlayabilmek adına File Transfer Protocol (FTP) hakkında bilgi sahibi olmak gerekmektedir.
#### 1.1.	File Transfer Protocol
FTP iki cihaz arasında çift yönlü olarak dosya aktarımını sağlamak için geliştirilen internet protokolüdür. Bilgisayar adresleri, kullanıcı bilgileri gibi bilgiler üzerinden işlemler gerçekleştirilir [1]. 

Bir FTP programında kullanılan komutlar aşağıda listelenmiştir. Komutlar ve kullanım şekillerini içeren liste KAYNAKLAR başlığı altında yer alan [2] numaraları kaynaktan düzenlenmiştir. 

| Komut | Kullanım Şekli |
| ------ | ------ |
|	cd |Dizin adresini değiştirmek için kullanılır.| 
|	pwd | İçinde bulunmakta olduğumuz dizinin ismini verir.|||
|	dir | Dizin içerisinde bulunan dosyaları listelememek için kullanılır.||
|	ls| Dizin içindeki çok fazla miktarda dosya bulunması durumunda sayfa sayfa listeleme için kullanılır.|
|	get| Dosya alma işlemi için kullanılır.|
|	mget| Çok sayıda dosya almak için kullanılır.|
|	put|Dosya göndermek için kullanılır.|
|	mput| Çok sayıda dosya göndermek için kullanılır.|
|	ascii| Dosyaların ASCII modu olarak aktarılacağını belirtir.|
|	binary| Dosyaların arşiv dosyası, çalışabilir program (.exe vb.) ve resim formatlı bir şekilde binary larak gönderileceğini belirtir.|
|	delete| İstenilen dosyayı silme komutudur.|
|	mkdir|FTP yapılan yer için yeni dizin oluşturma komutudur.|
|	rmdir| FTP yapılan yer için boş bulunan dizini silme komutudur.|
|	lcd| Kendi makineniz için dizin değiştirmenizi sağlayan komuttur.|
|	close| Ortamdan çıkmadan ilgili ortamın kapatılmasına olanak sağlayan komuttur.|
|	quit| Ortamı ve programı kapatmak için kullanılan komuttur.|

Verilen komutlar oluşturulan program için de kullanılmıştır. Programa ait kodların ve programın işleyişinin açıklaması 1.2 Program Hakkında başlığı altında bulunmaktadır.


#### 1.2.	Programın Oluşturulması

Programın çalışabilmesi için gerekli kütüphane olan ftplib programa import edilerek çalışılmaya başlanmıştır.

```sh
$ import ftplib
```

Sonraki adımda yapılan işlem programın FTP adresinin kontrolünü sağlayan kısımdır. Bı kısım adresin kullanıcıdan istenmesiyle başlar. Sonrasında kullanıcı bilgilerinin kontrolünü sağlar. Kullanıcı bilgileri doğruysa bilgilerin doğru olduğuna ve bağlantının doğru bir şekilde gerçekleştirildiğine dair bildirimde bulunur. Yanlış bilgilerin girilmesi durumunda ise kullanıcıya hata mesajı yollar ve bilgilerin tekrar edilmesini ister. 

```sh
def ftp_connect():
    while True:
        site_address = input('Please enter FTP address: ')
        try:
            with ftplib.FTP(site_address) as ftp:
                ftp.login()
                print(ftp.getwelcome())
                print('Current Directory', ftp.pwd())
                ftp.dir()
                print('Valid commands are cd/get/ls/exit - ex: get readme.txt')
                ftp_command(ftp)
                break 
        except ftplib.all_errors as e:
            print('Failed to connect!', e)
```

Erişimin sağlanması durumunda “readme.text” dosyasına bağlantı sağlanmış olur. Dosya siteden proje dosyasına çekilir. Böylece sunucu bağlantısı ve login işlemi sağlanmış olur. Ayrıca dosya bağlantısı ile bilgilerin çekilmesi de sağlanmıştır. Böylece bağlantı fonksiyonumuz görevini yerine getirmiş olur.

Dosya bağlantısının sağlanmasından sonraki bu kısım, önceki başlıkta belirttiğimiz komutları kullanarak işlem yapacağımız kısmı açmamıza olanak sağlamıştır.

Erişilen FTP sunucu üzerinde komutları kullanarak işlem yapabilmek için öncelikle programımız içerisinde bu komutları tanımlamamız gerekmektedir. Bu amaçla, programın ikinci kısmında oluşturulan fonksiyon komut fonksiyonudur. 

```sh
def ftp_command(ftp):
    while True:  # Run until 'exit' command is received from user
        command = input('Enter a command: ')
        commands = command.split()  # split command and file/directory into list
```

Oluşturulan fonksiyon while kontrol yapısı içerisinde oluşturulmuştur. Böylece, çıkış komutu gelene kadar programın çalışabilmesi sağlanmıştır. Kısacası program başlatıldığında işlemlerin sağlanması bu bölümdedir diyebiliriz. Komutların girilmesi işlemi sonrasında alınan komut girdisi listeye alınarak adres üzerinden işlem sağlanması amaçlanır. 

Komutlar üzerinden işlem yapabilmek için komutların ayrı ayrı tanımlanması gerekmektedir. Bu nedenle kontrol yapısı oluşturmak doğru olacaktır. Bu doğrultuda if-else yapıları kullanılarak tanımlamalar gerçekleştirilmiştir. Oluşturulan commands liste değişkeninin ne olduğu kontrol edilerek ona göre yönlendirme yapılacaktır.

```sh
 if commands[0] == 'cd': 
            try:
                ftp.cwd(commands[1])
                print('Directory of', ftp.pwd())
                ftp.dir()
                print('Current Directory', ftp.pwd())
            except ftplib.error_perm as e:  
                error_code = str(e).split(None, 1)
                if error_code[0] == '550':
                    print(error_code[1], 'Directory may not exist or you may not have permission to view it.')

```
İlk tanımlanan komut cd komutudur. Komut dizinin adresini değiştirmek için kullanılır. Bu nedenle ilgili port dinlenir ve öncelikle bulunulan dizin kullanıcıya gösterilir. Sonrasında, girilen bulunulan adres eşleşmeleri ile ilgili işlem yapılır. Kullanılan adreste dizine ulaşmak için o adresin ismi yazılmalıdır. Bizim sunucumuz için cd debian komutu kullanılır olacaktır.

Komutun girilmesi ile kullanıcı içerisinde bulunan debian adresine erişim sağlanmıştır. Sonrasında dosya içerisinde yer alan dosyalar ve boyutları kullanılacak komutları ile listelenmiş olur. Böylece istenilen alt dizinlere de erişim sağlanmasına imkan sağlanır.
  
Alt dizin olarak Şekil 1.1’de bulunan listeden yola çıkarak tools alt dizinine ulaşmak istediğimizde, debian içerisinde bulunduğumuzdan dolayı sadece tools yazmamız yeterli olacaktır. Bu komut bizi sunucuda bulunan “/debian/tools” adresine yönlendirecektir. Komutun girilmesi ile dizin içerisinde yer alan dosyalar listelenmiş olacaktır. 

Kod içerisinde tanımlanan bir diğer komut get komutudur. Daha önce de belirtildiği gibi bu komut dosya indirilmesine olanak sağlar.  Yapılması gereken ilk iş indirmek istediğimiz dosyanın bulunduğu dizini açmaktır. Kullanılan cd komutu bu işlem için yardımcı olacaktır. İndirmek istenilen dosyanın get komutundan sonra yazılmasıyla indirme işlemi sağlanmış olur. İndirmenin başarılı olma durumunda kullanıcıya bu durumla ilgili mesaj yollanır. Eğer istenilen dizin kullanıma uygun değil veya yanlış adreslenmiş ise hata mesajı kullanıcıya gösterilir.

```sh
elif commands[0] == 'get':  
                ftp.retrbinary('RETR ' + commands[1], open(commands[1], 'wb').write)
                print('File successfully downloaded.')
            except ftplib.error_perm as e
                error_code = str(e).split(None, 1)
                if error_code[0] == '550':
                    print(error_code[1], 'File may not exist or you may not have permission to view it.')

```

Örnek için debian dizininde bulunan README dosyasını ele alalım. Sunucuda dosyanın bulunduğu dizini açtıktan sonra get README yazmak yeterli olacaktır. Sonrasında kod içerisinde tanımladığımız indirme başarılı mesajı kullanıcıya gösterilir.Program içerisinde sağlanan listeleme ls ve exit komutları için else if metotları da şekilde gösterilmiştir.
 
 ```sh
elif commands[0] == 'ls':  
            ftp.dir()
        elif commands[0] == 'exit':  
            print('Goodbye!')
            break
```
Örneklenenler dışında düğer komutlar da kullanılabilir durumdadır. Dizine uygulanarak sonuçlar elde edilir. Sonrasında çıkış işlemi ile program sonlandırılır. 

### Sonuç
Projeyi özetlemek gerekirse, program ftp.debian.org üzerinde oluşturulan online bir sunucuya yönlendirilmiştir. Bu sunucu Debian işletim sisteminin FTP kullanıcıları için erişim sağladığı bir sunucudur. Yazılan kodların tamamı EKLER kısmında bulunmaktadır. Program ile ilgili sunucuya login işlemi sağlanmış ve bağlantı kurulumu gerçekleştirilmiştir. Sonrasında ilgili komutlardan birkaçı denenerek programın çalışması 2.2. Programın Oluşturulması başlığı altında örneklendirilmiştir. Kullanılır komutlar 2.1. File Transfer Protocol başlığı altında listelenmiştir. İlgili komutların çalışmasını sağlayan kütüphane Python içerisinde tanımlı ftplib kütüphanesindir. Kütüphane, programın sunucu üzerinde komutları uygulayabilmesine olanak sağlamıştır.
