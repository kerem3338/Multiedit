import os
import sys
import getpass
import settings
global commands

global cls


def cls():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


class DocumentManager:
    def __init__(self, mode):
        self.mode = mode
        self.data = {"docname": "doc", "author": getpass.getuser()}
        self.lines = {}
        self.file = None
        self.orginal = {}
        self.current = 0
        self.writerinfo = """Metin Düzenleyici
Komutlar

NOT: satırlar numaraları sıfırdan başlamaktadır

Kullanım:
	<satır> <içerik> :: satırın içeriğini değiştirir
Örnek:
	0 Merhaba Dünya

Komutlar
!close :: düzenleyiciyi moddan çıkış yapar.
!title <başlık> :: Dökümanın başlığını değiştirir.
!reset <satır> :: Satırı orjinal satır ile değiştirir.
!ln <satır> :: Satırı görüntüler.
!list :: Dosya içeriğini görüntüler.
!cls :: Ekranı temizler.
!help :: Yardım mesajını görüntüler.
"""
        self.do()

    def writetofile(self):
        """
Writes document content to file.
        """
        #Dosyanın var olup olmadığını kontrol et
        if os.path.exists(self.data["docname"]):
            if self.mode == "open":
                pass
            else:
                print(
                    f"{self.data['docname']} zaten var yeni bir dosya isimi gerekiyor")
                try:
                    name = input(">")
                except Exception as e:
                    print(e)
                else:
                    self.data["docname"] = name

        with open(self.data["docname"], "w",encoding=settings.encoding) as f:
            for line in range(len(list(self.lines.keys()))):
                if not line in self.lines:
                    self.lines.pop(line)
                else:
                    f.write(self.lines[line]+"\n")
    #Komutlar
    def commandchecker(self,linecontent):
        if linecontent == "!close":
            return "break"

        elif linecontent=="!list":
            for i in range(len(list(self.lines.keys()))):
                print(self.lines[i])

        elif linecontent=="!cls":
            cls()
        
        elif linecontent=="!execute":
            while True:
                try:
                    x=input(">")
                    if x==".exit":
                        break
                    else:
                        eval(x)
                except Exception as e:
                    print(e)
                
        elif linecontent=="!help":
            print(self.writerinfo)

        elif linecontent.split()[0]=="!ln":
            #girilen veri intiger'a çeviriliyor
            try:
                line=int(linecontent.split()[1])
            except ValueError:
                print("Please enter a intiger")

            #Eğer satır yok ise
            if not line in self.lines:
                print(f"ln command error: line '{line}' not found")
            else:
                print(self.lines(line))
        
         
        elif linecontent[0::6] == "!reset":
            if not self.mode == "open":
                print("'open' modu ile açınız")
            else:
                try:
                    line = linecontent.split()[1]
                    line = int(line)
                except Exception as e:
                    print(e)
                except IndexError:
                    print("Argument Required!")
                except ValueError:
                    print("Only Intiger!")
                else:
                    if line in list(self.orginal.keys()):
                        if line in list(self.lines.keys()):
                            self.line[line] = self.orginal[line]
                        else:
                            print("Satır Düzenlenmiş dosyada bulunamadı")
                    else:
                        print("Satır dosyada bulunamadı")
        else:
            print("Command Not Found")

    def fillblanklines(self):
        last=None
        for i in list(self.lines.keys()):
                if i == 0:
                    last=0
                else:
                    if i-last == 1:
                        pass
                    else:
                        for x in range(i-last):
                            if x ==0:
                                continue
                            self.lines[last+x]=" "
                
 
    def writer(self):
        """
        """
        print(self.writerinfo)
        if self.mode == "open":
            for i in range(len(list(self.lines.keys()))):
                self.current = i
            #self.current += 1
        print(self.current)
        while True:
            self.fillblanklines()
            linecontent = input(f"{self.current} ::")
            self.fillblanklines()
            if linecontent.startswith("!"):
                do=self.commandchecker(linecontent)
                if do == "break":
                    break
            else:
                try:
                    line = linecontent.split()[0]
                    line = int(line)
                    self.current = line
                except IndexError:
                    print("line mumber required")
                except ValueError:
                    print("line number required")
                else:
                    content = ""
                    for i in range(len(linecontent.split()[1::])):
                        content += linecontent.split()[1::][i]+" "
                    self.lines[self.current] = content
            self.fillblanklines()
            #self.lines[int(self.current)] = linecontent
            # self.current=len(list(self.lines.keys()))
        self.fillblanklines()
        q = input("Okumak ister misiniz (E/H)")
        if q == "e":
            for i in range(len(list(self.lines.keys()))):
                print(self.lines[i])
        else: 
            pass
        try:
            self.writetofile()
        except Exception as e:
            print("ERROR: "+str(e))
        else:
            print("Dosya başarı ile kayıt edildi")

    def do(self):
        if self.mode == "new":
            self.writer()
        elif self.mode == "open":
            filename = input("dosya:")
            if not os.path.exists(filename):
                print("Dosya bulunamadı")
            else:
                self.data["docname"] = filename
                self.file = open(self.data["docname"], "r+")
                with open(self.data["docname"], "r+") as f:
                    lines = f.readlines()
                    for i in range(len(lines)):
                        self.lines[i] = lines[i]
                        self.orginal[i] = lines[i]
                self.writer()
        else:
            print("MODE ERROR!")


commands = {
    "new": {"name": "new", "call": DocumentManager, "args": ["new"], "desc": "Create New doc."},
    "open": {"name": "open", "call": DocumentManager, "args": ["open"], "desc": "Open file"}

}


def getlistofcommands():
    for line in range(len(list(commands.keys()))):
        data = commands[list(commands.keys())[line]]
        print(f"{data['name']} -- {data['desc']}")


def runcommand(name):
    if name in commands:
        commands[name]["call"](*commands[name]["args"])
    else:
        print("Command not found")


getlistofcommands()
while True:
    try:
        inp = input(">>")
        runcommand(inp)
    except KeyboardInterrupt:
        sys.exit()

        