# script para automatizar o deploy do app
import os
os.system("git pull")
# os.system("buildozer -v android clean")
# apagar o arquivo de log
if os.path.exists("log.txt"):
    os.remove("log.txt")
os.system("nohup buildozer -v android debug > log.log &")

# verificar se no arquivo de log tem a palavra "APK"
while True:
    if os.path.exists("log.txt") and "# APK inclusiveway-0.1-arm64-v8a_armeabi-v7a-debug.apk available in the bin directory" in open("log.txt").read():
        os.system("git add .")
        os.system("git commit -m 'Atualizando'")
        os.system("git push")
        numero = "0.0.13"
        os.system("gh release create v0.0.1 '/home/ubuntu/ask/bin/inclusiveway-0.1-arm64-v8a_armeabi-v7a-debug.apk'")
        # interagindo com o terminal para colocar a realease no github
        '''
        ? Title (optional) v0.0.8 = escrever v0.0.8 + enter
        ? Release notes Leave blank = seta para cima + enter
        ? Is this a prerelease? Yes = escrever yes + enter
        ? Submit? Publish release = enter
        '''
        break

# wget https://repo1.maven.org/maven2/com/graphhopper/graphhopper-web/8.0/graphhopper-web-8.0.jar https://raw.githubusercontent.com/graphhopper/graphhopper/8.x/config-example.yml https://download.geofabrik.de/south-america/brazil/norte-latest.osm.pbf
# java -D"dw.graphhopper.datareader.file=norte-latest.osm.pbf" -jar graphhopper*.jar server config-example.yml