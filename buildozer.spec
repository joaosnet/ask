[app]

# (str) Título do seu aplicativo
title = InclusiveWay

# (str) Nome do pacote
package.name = inclusiveway

# (str) Domínio do pacote (necessário para empacotamento android/ios)
package.domain = ask.test

# (str) Código-fonte onde o main.py está localizado
source.dir = .

# (list) Arquivos de origem para incluir (deixe vazio para incluir todos os arquivos)
source.include_exts = py,png,jpg,kv,atlas, refresh_token.txt, usuario.txt

# (list) Lista de inclusões usando correspondência de padrões
# source.include_patterns = icones/*.png

# (list) Arquivos de origem para excluir (deixe vazio para não excluir nada)
#source.exclude_exts = spec

# (list) Lista de diretórios para excluir (deixe vazio para não excluir nada)
#source.exclude_dirs = tests, bin, venv

# (list) Lista de exclusões usando correspondência de padrões
# Não prefixe com './'
#source.exclude_patterns = license,images/*/*.jpg

# (str) Versionamento do aplicativo (método 1)
version = 0.1

# (str) Versionamento do aplicativo (método 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Requisitos do aplicativo
# separados por vírgula, por exemplo, requirements = sqlite3,kivy
requirements = kivy==master, https://github.com/kivymd/KivyMD/archive/master.zip, requests==2.31.0, mapview==1.0.6, https://github.com/HyTurtle/plyer/archive/master.zip, watchdog, redis, googlemaps, async_timeout
# (str) Pastas de origem personalizadas para requisitos
# Define a origem personalizada para quaisquer requisitos com receitas
# requirements.source.kivy = ../../kivy

# (str) Presplash do aplicativo
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Ícone do aplicativo
icon.filename = %(source.dir)s/images/1_APP.png

# (list) Orientações suportadas
# Opções válidas são: landscape, portrait, portrait-reverse ou landscape-reverse
orientation = portrait

# (list) Lista de serviços a declarar
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

#
# Específico do OSX
#

#
# author = © Informações de direitos autorais

# altera a versão principal do python usada pelo aplicativo
osx.python_version = 3.10

# versão do Kivy a ser usada
osx.kivy_version = 2.3

#
# Específico do Android
#

# (bool) Indica se o aplicativo deve ser em tela cheia ou não
fullscreen = 0

# (string) Cor de fundo do presplash (para a cadeia de ferramentas android)
# Formatos suportados são: #RRGGBB #AARRGGBB ou um dos seguintes nomes:
# red, blue, green, black, white, gray, cyan, magenta, yellow, lightgray,
# darkgray, grey, lightgrey, darkgrey, aqua, fuchsia, lime, maroon, navy,
# olive, purple, silver, teal.
#android.presplash_color = #FFFFFF

# (string) Animação de presplash usando formato Lottie.
# veja https://lottiefiles.com/ para exemplos e https://airbnb.design/lottie/
# para documentação geral.
# Os arquivos Lottie podem ser criados usando várias ferramentas, como Adobe After Effect ou Synfig.
android.presplash_lottie = %(source.dir)s/images/maprouteanimation.json

# (str) Ícone adaptável do aplicativo (usado se o nível de API do Android for 26+ em tempo de execução)
#icon.adaptive_foreground.filename = %(source.dir)s/data/icon_fg.png
#icon.adaptive_background.filename = %(source.dir)s/data/icon_bg.png

# (list) Permissões
# (Veja https://python-for-android.readthedocs.io/en/latest/buildoptions/#build-options-1 para todas as sintaxes e propriedades suportadas)
android.permissions = android.permission.INTERNET, (name=android.permission.WRITE_EXTERNAL_STORAGE;maxSdkVersion=18), android.permission.ACCESS_COARSE_LOCATION, android.permission.ACCESS_FINE_LOCATION

# (list) recursos compartilhados do Android que serão adicionados ao AndroidManifest.xml usando a tag <uses-library>
#android.uses_library =

# (int) API Android de destino, deve ser o mais alto possível.
android.api = 33

# (int) API mínima que seu APK / AAB suportará.
# android.minapi = 31

# (int) Versão do SDK do Android a ser usada
#android.sdk = 20

# (str) Versão do NDK do Android a ser usada
#android.ndk = 23b

# (int) API NDK do Android a ser usada. Esta é a API mínima que seu aplicativo suportará, geralmente deve corresponder a android.minapi.
#android.ndk_api = 21

# (bool) Use armazenamento de dados --private (True) ou --dir armazenamento público (False)
#android.private_storage = True

# (str) Diretório NDK do Android (se vazio, será baixado automaticamente.)
#android.ndk_path =

# (str) Diretório SDK do Android (se vazio, será baixado automaticamente.)
#android.sdk_path =

# (str) Diretório ANT (se vazio, será baixado automaticamente.)
#android.ant_path =

# (bool) Se True, então pule a tentativa de atualizar o SDK do Android
# Isso pode ser útil para evitar downloads excessivos da Internet ou economizar tempo
# quando uma atualização é devida e você só quer testar/construir seu pacote
# android.skip_update = False

# (bool) Se True, então aceite automaticamente as licenças do SDK
# acordos. Isso é destinado apenas para automação. Se definido como False,
# o padrão, você verá a licença quando executar o
# buildozer pela primeira vez.
# android.accept_sdk_license = False

# (str) Ponto de entrada do Android, o padrão é ok para aplicativos baseados em Kivy
#android.entrypoint = org.kivy.android.PythonActivity

# (str) Nome completo incluindo o caminho do pacote da classe Java que implementa a atividade Android
# use esse parâmetro junto com android.entrypoint para definir uma classe Java personalizada em vez de PythonActivity
#android.activity_class_name = org.kivy.android.PythonActivity

# (str) XML extra para escrever diretamente dentro do elemento <manifest> de AndroidManifest.xml
# use esse parâmetro para fornecer um nome de arquivo de onde carregar seu código XML personalizado
#android.extra_manifest_xml = ./src/android/extra_manifest.xml

# (str) XML extra para escrever diretamente dentro da tag <manifest><application> de AndroidManifest.xml
# use esse parâmetro para fornecer um nome de arquivo de onde carregar seus argumentos XML personalizados:
#android.extra_manifest_application_arguments = ./src/android/extra_manifest_application_arguments.xml

# (str) Nome completo incluindo o caminho do pacote da classe Java que implementa o serviço Python
# use esse parâmetro para definir uma classe Java personalizada que estende PythonService
#android.service_class_name = org.kivy.android.PythonService

# (str) Tema do aplicativo Android, o padrão é ok para aplicativos baseados em Kivy
# android.apptheme = "@android:style/Theme.NoTitleBar"

# (list) Padrão para lista branca para todo o projeto
#android.whitelist =

# (str) Caminho para um arquivo de lista branca personalizado
#android.whitelist_src =

# (str) Caminho para um arquivo de lista negra personalizado
#android.blacklist_src =

# (list) Lista de arquivos .jar Java para adicionar às bibliotecas para que pyjnius possa acessar
# suas classes. Não adicione jars que você não precisa, pois jars extras podem diminuir
# o processo de construção. Permite correspondência de curingas, por exemplo:
# OUYA-ODK/libs/*.jar
#android.add_jars = foo.jar,bar.jar,path/to/more/*.jar

# (list) Lista de arquivos Java para adicionar ao projeto Android (pode ser java ou um
# diretório contendo os arquivos)
#android.add_src =

# (list) Arquivos AAR do Android para adicionar
#android.add_aars =

# (list) Coloque esses arquivos ou diretórios no diretório de ativos do apk.
# Qualquer forma pode ser usada e os ativos não precisam estar em 'source.include_exts'.
# 1) android.add_assets = source_asset_relative_path
# 2) android.add_assets = source_asset_path:destination_asset_relative_path
#android.add_assets =

# (list) Coloque esses arquivos ou diretórios no diretório res do apk.
# A opção pode ser usada de três maneiras, o valor pode conter um ou zero ':'
# Alguns exemplos:
# 1) Um arquivo para adicionar aos recursos, nomes de recursos legais contêm ['a-z', '0-9', '_']
# android.add_resources = my_icons/all-inclusive.png:drawable/all_inclusive.png
# 2) Um diretório, aqui 'legal_icons' deve conter recursos de um tipo
# android.add_resources = legal_icons:drawable
# 3) Um diretório, aqui 'legal_resources' deve conter um ou mais diretórios,
# cada um de um tipo de recurso: desenhável, xml, etc ...
# android.add_resources = legal_resources
#android.add_resources =

# (list) Dependências do Gradle para adicionar
#android.gradle_dependencies =

# (bool) Habilitar suporte AndroidX. Habilitar quando 'android.gradle_dependencies'
# contém um pacote 'androidx' ou qualquer pacote de fonte Kotlin.
# android.enable_androidx requer android.api >= 28
#android.enable_androidx = True

# (list) adicionar opções de compilação java
# isso pode, por exemplo, ser necessário ao importar certas bibliotecas java usando a opção 'android.gradle_dependencies'
# consulte https://developer.android.com/studio/write/java8-support para mais informações
# android.add_compile_options = "sourceCompatibility = 1.8", "targetCompatibility = 1.8"

# (list) Repositórios Gradle para adicionar {pode ser necessário para algumas android.gradle_dependencies}
# por favor, coloque entre aspas duplas
# por exemplo, android.gradle_repositories = "maven { url 'https://kotlin.bintray.com/ktor' }"
#android.add_gradle_repositories =

# (list) opções de empacotamento para adicionar
# consulte https://google.github.io/android-gradle-dsl/current/com.android.build.gradle.internal.dsl.PackagingOptions.html
# pode ser necessário para resolver conflitos em gradle_dependencies
# por favor, coloque entre aspas duplas
# por exemplo, android.add_packaging_options = "exclude 'META-INF/common.kotlin_module'", "exclude 'META-INF/*.kotlin_module'"
#android.add_packaging_options =

# (list) Classes Java para adicionar como atividades ao manifesto.
#android.add_activities = com.example.ExampleActivity

# (str) Categoria do console OUYA. Deve ser um dos JOGO ou APP
# Se você deixar isso em branco, o suporte OUYA não será ativado
#android.ouya.category = GAME

# (str) Nome do arquivo de ícone do console OUYA. Deve ser uma imagem png de 732x412.
#android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) Arquivo XML para incluir como filtros de intenção na tag <activity>
#android.manifest.intent_filters =

# (list) Copie esses arquivos para src/main/res/xml/ (usado, por exemplo, com filtros de intenção)
#android.res_xml = PATH_TO_FILE,

# (str) launchMode para definir para a atividade principal
#android.manifest.launch_mode = standard

# (str) screenOrientation para definir para a atividade principal.
# Valores válidos podem ser encontrados em https://developer.android.com/guide/topics/manifest/activity-element
#android.manifest.orientation = fullSensor

# (list) Bibliotecas adicionais do Android para copiar em libs/armeabi
#android.add_libs_armeabi = libs/android/*.so
#android.add_libs_armeabi_v7a = libs/android-v7/*.so
#android.add_libs_arm64_v8a = libs/android-v8/*.so
#android.add_libs_x86 = libs/android-x86/*.so
#android.add_libs_mips = libs/android-mips/*.so

# (bool) Indique se a tela deve permanecer ligada
# Não se esqueça de adicionar a permissão WAKE_LOCK se definir isso como True
#android.wakelock = False

# (list) Metadados do aplicativo Android para definir (formato chave = valor)
#android.meta_data =

# (list) Projeto de biblioteca Android para adicionar (será adicionado em
# project.properties automaticamente.)
#android.library_references =

# (list) Bibliotecas compartilhadas do Android que serão adicionadas ao AndroidManifest.xml usando a tag <uses-library>
#android.uses_library =

# (str) Filtros logcat do Android para usar
android.logcat_filters = *:S python:D

# (bool) Android logcat exibe apenas log para o pid da atividade
#android.logcat_pid_only = False

# (str) Argumentos adb adicionais do Android
#android.adb_args = -H host.docker.internal

# (bool) Copie a biblioteca em vez de fazer um libpymodules.so
#android.copy_libs = 1

# (list) As arquiteturas Android para compilar, escolhas: armeabi-v7a, arm64-v8a, x86, x86_64
# No passado, era `android.arch` como não estávamos suportando compilações para várias arquiteturas ao mesmo tempo.
android.archs = arm64-v8a, armeabi-v7a

# (int) substitui o cálculo automático de versionCode (usado em build.gradle)
# isso não é o mesmo que a versão do aplicativo e só deve ser editado se você souber o que está fazendo
# android.numeric_version = 1

# (bool) habilita o recurso de backup automático do Android (Android API> = 23)
android.allow_backup = True

# (str) arquivo XML para regras de backup personalizadas (consulte a documentação oficial de backup automático)
# android.backup_rules =

# (str) Se você precisar inserir variáveis em seu arquivo AndroidManifest.xml,
# você pode fazer isso com a propriedade manifestPlaceholders.
# Esta propriedade recebe um mapa de pares chave-valor. (via uma string)
# Exemplo de uso: android.manifest_placeholders = [myCustomUrl: \"org.kivy.customurl\"]
# android.manifest_placeholders = [:]

# (bool) Ignorar a compilação de bytes para arquivos .py
# android.no-byte-compile-python = False

# (str) O formato usado para empacotar o aplicativo para o modo de lançamento (aab ou apk ou aar).
# android.release_artifact = aab

# (str) O formato usado para empacotar o aplicativo para o modo de depuração (apk ou aar).
# android.debug_artifact = apk

#
# Python para android (p4a) específico
#

# (str) URL do python-for-android para usar para checkout
#p4a.url =

# (str) python-for-android fork a ser usado no caso de p4a.url não ser especificado, padrão para upstream (kivy)
#p4a.fork = kivy

# (str) ramo python-for-android a ser usado, padrão para mestre
#p4a.branch = master

# (str) commit específico do python-for-android a ser usado, padrão para HEAD, deve estar dentro de p4a.branch
#p4a.commit = HEAD

# (str) diretório de clone git python-for-android (se vazio, será automaticamente clonado do github)
#p4a.source_dir =

# (str) O diretório em que python-for-android deve procurar suas próprias receitas de construção (se houver)
#p4a.local_recipes =

# (str) Nome do arquivo de gancho para p4a
#p4a.hook =

# (str) Bootstrap a ser usado para compilações android
# p4a.bootstrap = sdl2

# (int) número de porta para especificar um argumento explícito --port= p4a (por exemplo, para bootstrap flask)
#p4a.port =

# Controle de passagem --use-setup-py vs --ignore-setup-py para p4a
# "no futuro" --use-setup-py será o comportamento padrão em p4a, agora não é
# Definir isso como falso passará --ignore-setup-py, verdadeiro passará --use-setup-py
# NOTA: esta é uma integração geral do setuptools, ter pyproject.toml é suficiente, não é necessário gerar
# setup.py se você estiver usando Poetry, mas você precisa adicionar "toml" a source.include_exts.
#p4a.setup_py = false

# (str) argumentos adicionais da linha de comando para passar ao invocar a ferramenta pythonforandroid
#p4a.extra_args =



#
# iOS específico
#

# (str) Caminho para uma pasta kivy-ios personalizada
#ios.kivy_ios_dir = ../kivy-ios
# Alternativamente, especifique a URL e o ramo de um checkout git:
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master

# Outra dependência de plataforma: ios-deploy
# Descomente para usar um checkout personalizado
#ios.ios_deploy_dir = ../ios_deploy
# Ou especifique URL e ramo
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0

# (bool) Se deve ou não assinar o código
ios.codesign.allowed = false

# (str) Nome do certificado a ser usado para assinar a versão de depuração
# Obtenha uma lista de identidades disponíveis: buildozer ios list_identities
#ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (<hexstring>)"

# (str) A equipe de desenvolvimento a ser usada para assinar a versão de depuração
#ios.codesign.development_team.debug = <hexstring>

# (str) Nome do certificado a ser usado para assinar a versão de lançamento
#ios.codesign.release = %(ios.codesign.debug)s

# (str) A equipe de desenvolvimento a ser usada para assinar a versão de lançamento
#ios.codesign.development_team.release = <hexstring>

# (str) URL apontando para o arquivo .ipa a ser instalado
# Esta opção deve ser definida junto com as opções 'display_image_url' e 'full_size_image_url'.
#ios.manifest.app_url =

# (str) URL apontando para um ícone (57x57px) a ser exibido durante o download
# Esta opção deve ser definida junto com as opções 'app_url' e 'full_size_image_url'.
#ios.manifest.display_image_url =

# (str) URL apontando para um ícone grande (512x512px) a ser usado pelo iTunes
# Esta opção deve ser definida junto com as opções 'app_url' e 'display_image_url'.
#ios.manifest.full_size_image_url =


[buildozer]

# (int) Nível de log (0 = apenas erro, 1 = informações, 2 = depuração (com saída de comando))
log_level = 2

# (int) Exibir aviso se o buildozer for executado como root (0 = Falso, 1 = Verdadeiro)
warn_on_root = 1

# (str) Caminho para armazenamento de artefatos de construção, absoluto ou relativo ao arquivo de especificação
# build_dir = ./.buildozer

# (str) Caminho para armazenamento de saída de construção (ou seja, .apk, .aab, .ipa)
# bin_dir = ./bin

#    -----------------------------------------------------------------------------
#    Liste como seções
#
#    Você pode definir todas as "listas" como [seção: chave].
#    Cada linha será considerada como uma opção para a lista.
#    Vamos pegar [app] / source.exclude_patterns.
#    Em vez de fazer:
#
#[app]
#source.exclude_patterns = license,data/audio/*.wav,data/images/original/*
#
#    Isso pode ser traduzido em:
#
#[app:source.exclude_patterns]
#license
#data/audio/*.wav
#data/images/original/*
#


#    -----------------------------------------------------------------------------
#    Perfis
#
#    Você pode estender a seção / chave com um perfil
#    Por exemplo, você deseja implantar uma versão de demonstração do seu aplicativo sem
#    conteúdo HD. Você poderia primeiro mudar o título para adicionar "(demo)" no nome
#    e estenda os diretórios excluídos para remover o conteúdo HD.
#
#[app@demo]
#title = My Application (demo)
#
#[app:source.exclude_patterns@demo]
#images/hd/*
#
#    Em seguida, invoque a linha de comando com o perfil "demo":
#
#buildozer --profile demo android debug
