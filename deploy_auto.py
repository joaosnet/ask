# script para automatizar o deploy do app
import os
os.system("ls -l")
os.system("git pull")
os.system("buildozer android clean")
os.system("buildozer android debug deploy run logcat > log.txt")
os.system("git add .")
os.system("git commit -m 'Atualizando'")
os.system("git push")
os.system("gh release create 0.0.1 '/home/ubuntu/ask/bin/inclusiveway-0.1-arm64-v8a_armeabi-v7a-debug.apk'")