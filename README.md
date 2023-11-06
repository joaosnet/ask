# InclusiveWay - Aplicativo para Melhorar a Mobilidade de Pessoas com Deficiência

<img align="right" height="256" src="https://github.com/joaosnet/ask/blob/main/images/1_APP.png"/>

## Descrição do Projeto

O projeto InclusiveWay da organização ASK visa melhorar a mobilidade de pessoas com deficiência visual no meio urbano, proporcionando uma solução inovadora para a locomoção em vias públicas. Com cerca de 250 milhões de pessoas com deficiência visual no mundo, e aproximadamente 45 milhões no Brasil, o aplicativo busca facilitar a vida dessas pessoas, oferecendo informações em tempo real sobre as condições das vias e alertas sobre obstáculos.

# Índice

* [Descrição do Projeto](#descrição-do-projeto)

* [Telas do Aplicativo](#telas-do-aplicativo)

* [Arquitetura do Aplicativo](#arquitetura-do-aplicativo)

* [Objetivos](#objetivos)

* [Integrantes do Grupo](#integrantes-do-grupo)

* [Slides do Projeto](#slides-do-projeto)

* [Como executar o Protótipo do Aplicativo](#como-executar-o-protótipo-do-aplicativo)

* [Como Contribuir](#como-contribuir)

* [Para construir uma versão no Buildozer](#para-construir-uma-versão-no-buildozer)

* [Para colocar em segundo plano no linux](#para-colocar-em-segundo-plano-no-linux)

* [Para atualizar o git](#para-atualizar-o-git)


## Telas do Aplicativo
![Telas](/icones/Telas.png)

_Telas_

## Arquitetura do Aplicativo
![Arquitetura](/images/arquitetura.png)

_Arquitetura_

## Objetivos

### Geral

Melhorar a mobilidade de pessoas com deficiência visual no meio urbano.

### Específicos

1. Fornecer alertas em tempo real sobre obstáculos nas vias.
2. Oferecer informações sobre a condição das vias para traçar rotas ideais.
3. Garantir acessibilidade completa por meio da compatibilidade com leitores de tela.

## Integrantes do Grupo

![Integrantes](/images/integrantes.png)

_Figure 1: Integrantes_

## Slides do Projeto

### Problema e Desafio Estratégico

![Problema](/images/problema.png)

_Figure 2: Problema em 1 slide_

### Solução e Proposta de Valor

![Solução](/images/solucao.png)

_Figure 3: Solução em 1 slide_

### Protótipo

![Protótipo](/images/prototipo.png)

_Figure 4: Protótipo em 1 slide_

## Como executar o Protótipo do Aplicativo

### No windows
1. Instale o [anaconda](https://docs.anaconda.com/free/anaconda/install/windows.html)
2. Crie um ambiente virtual
```bash
conda create -n ask python=3.10
```
3. Ative o ambiente virtual
```bash
conda activate ask
```
4. Instale as dependências
```bash
pip install -r requirements_windows.txt
```
5. Execute o aplicativo
```bash
python main.py
```

### No Linux
1. Instale o [anaconda](https://www.digitalocean.com/community/tutorials/how-to-install-the-anaconda-python-distribution-on-ubuntu-20-04-pt)
2. Crie um ambiente virtual
```bash
conda create -n ask python=3.10
```
3. Ative o ambiente virtual
```bash
conda activate ask
```
4. Instale as dependências
```bash
pip install -r requirements_linux.txt
```
5. Execute o aplicativo
```bash
python main.py
```

## Como Contribuir

Se você deseja contribuir para o desenvolvimento do aplicativo, siga os passos abaixo:

1. Faça um fork do repositório
2. Clone o fork para o seu ambiente local
3. Crie uma branch para suas alterações (`git checkout -b nome-da-sua-branch`)
4. Faça commit das suas alterações (`git commit -m 'Descrição das alterações'`)
5. Faça push para a branch (`git push origin nome-da-sua-branch`)
6. Abra um pull request no repositório original

## Para construir uma versão no Buildozer
- Modifique o arquivo (`buildozer.spec`)
### Para ver o erros e fazer uma criar uma versão.apk
```bash
buildozer android debug deploy run logcat
```

### Para ver os erros e o log em .txt
```bash
buildozer android debug deploy run logcat > log.txt
```
### Para construir apenas o arquivo .apk
```bash
buildozer -v android debug
buildozer android logcat > log.txt
```

### Sempre limpar o buildozer antes de fazer uma nova build
```bash
buildozer android clean
```

## Para colocar em segundo plano no linux
```bash
nohup buildozer -v android debug > log.txt &
```
### Para ver o log
```bash
tail -f log.txt
```

## Para atualizar o git
### Fazendo alterações no git
```bash
git pull
git add .
git commit -m "Atualizando"
git push
```
### Adicionando uma nova realease apenas do arquivo .apk gerado pelo buildozer no github
```bash
git tag -a v1.0 -m "Versão 1.0"
git push origin v1.0
```

