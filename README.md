# InclusiveWay - Aplicativo para Melhorar a Mobilidade de Pessoas com Deficiência

![GitHub repo size](https://img.shields.io/github/repo-size/joaosnet/ask?style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/joaosnet/ask?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/joaosnet/ask?style=for-the-badge)
![Bitbucket open issues](https://img.shields.io/bitbucket/issues/joaosnet/ask?style=for-the-badge)
![Bitbucket open pull requests](https://img.shields.io/bitbucket/pr-raw/joaosnet/ask?style=for-the-badge)

<img align="right" height="256" src="https://github.com/joaosnet/ask/blob/main/images/1_APP.png"/>

## Descrição do Projeto

O projeto InclusiveWay da organização ASK visa melhorar a mobilidade de pessoas com deficiência visual no meio urbano, proporcionando uma solução inovadora para a locomoção em vias públicas. Com cerca de 250 milhões de pessoas com deficiência visual no mundo, e aproximadamente 45 milhões no Brasil, o aplicativo busca facilitar a vida dessas pessoas, oferecendo informações em tempo real sobre as condições das vias e alertas sobre obstáculos.

# Índice

* [Descrição do Projeto](#descrição-do-projeto)

* [Telas do Aplicativo](#telas-do-aplicativo)

* [Arquitetura do Aplicativo](#arquitetura-do-aplicativo)

* [Objetivos](#objetivos)

* [🤝 Colaboradores](#-colaboradores)

* [Slides do Projeto](#slides-do-projeto)

* [☕ Usando o protótipo em python do InclusiveWay](#Usando_o_protótipo_em_python_do_InclusiveWay)

* [📫 Contribuindo para InclusiveWay](#Contribuindo_para_InclusiveWay)

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

## 🤝 Colaboradores

![Integrantes](/images/integrantes.png)

_Figure 1: Integrantes_

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/joaosnet" title="Perfil do Github do João Natividade">
        <img src="https://avatars.githubusercontent.com/u/87316339?v=4" width="100px;" alt="Foto do João Natividade no GitHub"/><br>
        <sub>
          <b>João Natividade</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#" title="defina o titulo do link">
        <img src="https://s2.glbimg.com/FUcw2usZfSTL6yCCGj3L3v3SpJ8=/smart/e.glbimg.com/og/ed/f/original/2019/04/25/zuckerberg_podcast.jpg" width="100px;" alt="Foto do Mark Zuckerberg"/><br>
        <sub>
          <b>Mark Zuckerberg</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#" title="defina o titulo do link">
        <img src="https://miro.medium.com/max/360/0*1SkS3mSorArvY9kS.jpg" width="100px;" alt="Foto do Steve Jobs"/><br>
        <sub>
          <b>Steve Jobs</b>
        </sub>
      </a>
    </td>
  </tr>
</table>

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

## ☕ Usando o protótipo em python do InclusiveWay

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

## 📫 Contribuindo para InclusiveWay

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
buildozer -v android clean
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
gh release create 0.0.1 '/home/ubuntu/ask/bin/inclusiveway-0.1-arm64-v8a_armeabi-v7a-debug.apk'
```

