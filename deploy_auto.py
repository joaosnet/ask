# script para automatizar o deploy do app
import os
os.system("git pull")
# os.system("buildozer android clean")
# apagar o arquivo de log
if os.path.exists("log.txt"):
    os.remove("log.txt")
os.system("nohup buildozer -v android debug > log.txt &")

# verificar se no arquivo de log tem a palavra "APK"
while True:
    if os.path.exists("log.txt") and "# APK inclusiveway-0.1-arm64-v8a_armeabi-v7a-debug.apk available in the bin directory" in open("log.txt").read():
        os.system("git add .")
        os.system("git commit -m 'Atualizando'")
        os.system("git push")
        numero = "0.0.13"
        os.system("gh release create v0.0.14 '/home/ubuntu/ask/bin/inclusiveway-0.1-arm64-v8a_armeabi-v7a-debug.apk'")
        # interagindo com o terminal para colocar a realease no github
        
        '''
        ? Title (optional) v0.0.8
        ? Release notes Leave blank
        ? Is this a prerelease? Yes
        ? Submit? Publish release
        '''
        break
