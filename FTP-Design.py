import ftplib
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

def ftp_command(ftp):
    while True:  #Programın durdurulana kadar çalışması sağlanır.
        command = input('Enter a command: ')
        commands = command.split()  #Kullanılmak istenilen komut değişkene atanır.

        if commands[0] == 'cd': #Adrese ulaşma sağlanır. Komutlar if- else kontrol yapıları ile oluşturulur. Böylece komutun doğruluğu kontrol edilir.

            try:
                ftp.cwd(commands[1])
                print('Directory of', ftp.pwd())
                ftp.dir()
                print('Current Directory', ftp.pwd())
            except ftplib.error_perm as e:  #ftplib içerisinde tanımlı hata mesajı
                error_code = str(e).split(None, 1)
                if error_code[0] == '550':
                    print(error_code[1], 'Directory may not exist or you may not have permission to view it.')
        elif commands[0] == 'get':  #dosyayı getirme-indirme komutu
            try:
                ftp.retrbinary('RETR ' + commands[1], open(commands[1], 'wb').write)
                print('File successfully downloaded.')
            except ftplib.error_perm as e:  #ilgili komudun ftplib içerisinde tanımlı hata mesajı                
error_code = str(e).split(None, 1)
                if error_code[0] == '550':
                    print(error_code[1], 'File may not exist or you may not have permission to view it.')
        elif commands[0] == 'ls':  #Kullanılan listeleme komutu
            print('Directory of', ftp.pwd())
            ftp.dir()
        elif commands[0] == 'exit':  #Programın kapatılması- durdurulması
            ftp.quit()
            print('Goodbye!')
            break
        else:
            print('Invalid command, try again (valid options: cd/get/ls/exit).')

print('Welcome to Python FTP')
ftp_connect()

