| | |
|---|---|
| <img src="img/logo_ufsc_transparente_quadrado.png" width="200"/> | <img src="img/logo_ine_transparente_quadrado.png" width="200"/> |

Programa de Pós-graduação em Ciência da Computação
Departamento de Informática e Estatística - INE

# Contagem de salgadinhos sortidos em caixas mistas

* **Vicente Knobel Borges**
* **Luiz Gustavo Coutinho Xavier**


## Descrição do problema
O problema escolhido para atividade consiste na identificação de salgadinhos em caixas sortidas, adotando como exemplo encomendas de salgados produzidas por uma padaria local. Apesar de considerar a produção de um comércio específico, o problema estende-se a indústria de alimentos de modo geral, ao permitir a separação de encomendas de forma mais ágil assegurando controle de qualidade, especialmente em períodos de maior demanda de produção. Caixas sortidas são usualmente encomendadas com 4 ou 5 classes de salgados distintos, e possuem um tamanho padrão para conter um máximo de até 100 salgados. Foi testada uma pipeline de visão computacional clásssica com segmentação por cor para isolar uma classe de salgado e operações de fechamento e abertura para isolar salgados individuais dentro da classe, e uma solução com *deep learning* onde foi realizado o *fine-tuning* do modelo RF-DETR, obtendo mAP@50:95 de 90,51% no dataset de teste.

## Paradigma da Visão Computacional Clássica

Para o escopo de problema nesta etapa do trabalho, considera-se a existência das seguintes classes:

* Croquete de carne
* Coxinha de frango
* Empada folhada
* Sanduíche colorido
* Sanduíche aberto (canapé de salame com palito acima)
* Canudinho

É importante destacar a similaridade entre classes de salgadinhos no que diz respeito a sua cor e formato, o que representa um maior desafio na resolução do problema. Croquetes de carne apesar de majoritariamente marrons, possuem pigmentos pastéis da mesma cor das coxinhas devido a farinha utilizada em sua fabricação. Coxinhas e empadas também possuem grande similaridade de formato e cor.

As imagens do dataset se encontram disponíveis no diretório **/dataset**, totalizando 21 imagens. Diversas combinações de organizações com as seis classes de salgadinhos foram exploradas, incluindo organizações mais simples com somente uma classe. As imagens foram capturadas em alta resolução ($4032 \times 3024$) por uma câmera de celular

| | |
|---|---|
| ![IMG_2426](img/IMG_2426.jpeg) | ![IMG_2432](img/IMG_2432.jpeg) |
| ![IMG_2435](img/IMG_2435.jpeg) | ![IMG_2441](img/IMG_2441.jpeg) |


### Solução com visão clássica
Como primeira solução, foi implementado um pipeline simples de processamento de imagem utilizando algoritmos clássicos de visão computacional com o objetivo de identificar uma classe de salgadinhos por vez. A primeira etapa deste pipeline consiste em uma segmentação por cor criando-se uma máscara binária para os valores de pixels dentro de uma faixa de valores em HSV, utilizando da função `cv2.inRange`. Na segunda etapa é realizada uma transformação no domínio do espaço de fechamento, que consiste na aplicação em sequência de uma operação morfológica de dilatação (ie copiar pixel sempre que encontrados pelo kernel convolucional) seguida de uma erosão (ie copiar pixel para imagem resultante somente quando igual a totalidade do kernel). Essa transformação tem como objetivo preencher buracos detectados após aplicação da máscara binária preservando a imagem em seu tamanho original. Como terceira etapa, foi aplicado um leve borramento na imagem `cv2.bilateralFilter` para em sequencia aplicar o algoritmo de detecção de bordas de Canny (`cv2.Canny`). Como última etapa é realizada uma contagem direta de elipses sobre os objetos remanescentes representando os salgadinhos da classe escolhida.


![diagrama](img/diagrama-simples.png)


Nesta primeira iteração não foi possível isolar os salgadinhos desejados com uma acurácia satisfatória, isto é, identificar somente os salgadinhos da classe escolhida sem resquícios de sombra ou pedaços de outros elementos. Como ilustrado, na tentativa de identificar salgadinhos do tipo Croquete, acabávamos sempre com resquícios de outros elementos após a segmentação de cor. Os melhores resultados foram obtidos com a faixa de valores HSV [8, 130, 10] e [24, 180, 140]. Mesmo após a execução em sequência do fechamento na intenção de preencher os buracos, a detecção de bordas por Canny não contornou elipses perfeitas. Idealmente pensou-se que este capaz de identificar as bordas de somente a classe de salgadinhos segmentadas, para que então em uma última etapa fosse possível realizar uma contagem direta de elipses, os únicos objetos remanescentes representando os salgadinhos da classe croquete.

| | |
|---|---|
| <img src="img/IMG_2426.jpeg" width="500"/> | <img src="img/b.png" width="500"/> |
| <img src="img/c.png" width="500"/> | <img src="img/d.png" width="500"/> |


## Paradigma de *Deep Learning*


### Metodologia


O desenvolvimento seguiu cinco etapas: (1) busca de imagens no Google; (2) geração de *novel view synthesis* com Nano Banana Pro; (3) labeling automático com SAM3; (4) refinamento no Label Studio; (5) treinamento com RF-DETR.


#### Geração do Dataset


Para esta etapa, foram estabelecidas 14 classes de salgadinhos: Bolinha de queijo, Canapé, Canudo, Coxinha, Croquete, Empadinha, Enroladinho de salsicha, Esfiha, Folhado, Pastelzinho, Pão de queijo, Quibe, Risoles e Sanduíche. Foram coletadas 30 imagens por classe, priorizando fotos com múltiplos exemplares em ângulo *top-down*.


![Imagens de coxinhas selecionadas](img/coxinhas_google.jpg)

*Imagens de coxinhas selecionadas do Google*


#### Novel View Synthesis


Para suprir a escassez de vistas superiores (perspectiva principal do caso de uso em padarias), foi utilizado o modelo Nano Banana Pro da Google para gerar quatro variações de cada imagem: vista lateral, *top-down* no chão, *top-down* com iluminação noturna, e *top-down* na disposição original.


![Imagens geradas pelo Nano Banana](img/nanoBanana.jpg)

*Imagens de coxinhas geradas pelo Nano Banana Pro*


#### Labeling com SAM3 e Refinamento


O SAM3 foi utilizado para segmentação automática com prompts como "food" ou "snacks", gerando bounding boxes no formato YOLO. O refinamento foi realizado no Label Studio, corrigindo classificações incorretas, especialmente no conjunto "grupo" que continha salgadinhos diversos.


![Bounding boxes geradas por SAM3](img/sam3_raw_bbox.png)

*Bounding boxes geradas automaticamente pelo SAM3*


![Label Studio](img/uso_label_studio.png)

*Interface de revisão no Label Studio*


#### Divisão do Dataset


Os dados foram separados em 70% treino, 15% validação e 15% teste, garantindo que imagens derivadas da mesma fonte não ficassem em conjuntos diferentes. Foram criadas versões multilabel (14 classes) e monolabel (classe única "Salgadinho") do *dataset*.


### Modelo RF-DETR


O modelo RF-DETR foi selecionado por ser: performante em sistemas com poucos recursos, de fácil implementação em Python, e open-source (Apache-2.0) sem restrições comerciais.

Alinhado com o objetivo de ter um modelo performante, foi escolhido o modelo **RF-DETR Small** como o padrão a ser avaliado, dentro da familia de modelos RF-DETR.


![Comparação mAP COCO](img/RFDETR_COCO_map.png)

*Comparação de métricas mAP no dataset COCO do modelo RF-DETR (Fonte: Roboflow)*


### Resultados


![Resultados de treino mono](img/smallmonolabel.png)

*Curvas de treinamento para o modelo monolabel*

![Resultados de treino multi](img/smallmultilabel.png)

*Curvas de treinamento para o modelo multilabel*


#### Modelo Monolabel


**Tabela 1 - Métricas do modelo monolabel**


| Conjunto | mAP@50:95 | mAP@50 | Precision | Recall |
|----------|-----------|--------|-----------|--------|
| Validação | 94,66% | 98,55% | 98,00% | 97,00% |
| Teste | 95,29% | 98,64% | 97,45% | 97,00% |


#### Modelo Multilabel


**Tabela 2 - Métricas por classe do modelo multilabel**


| Classe | mAP@50:95 (Val) | mAP@50:95 (Test) | Precision (Val) | Precision (Test) |
|--------|-----------------|------------------|-----------------|------------------|
| Bolinha de queijo | 75,52% | 86,90% | 54,46% | 85,54% |
| Canapé | 94,18% | 93,93% | 92,86% | 95,10% |
| Canudo | 89,91% | 95,30% | 94,78% | 99,35% |
| Coxinha | 74,24% | 89,85% | 34,05% | 90,83% |
| Croquete | 94,39% | 90,84% | 94,59% | 89,07% |
| Empadinha | 93,93% | 96,29% | 97,93% | 100,00% |
| Enroladinho | 91,87% | 87,96% | 97,80% | 98,05% |
| Esfiha | 94,57% | 98,85% | 99,22% | 99,53% |
| Folhado | 97,69% | 92,49% | 100,00% | 91,04% |
| Pastelzinho | 89,68% | 91,42% | 95,33% | 96,03% |
| Pão de queijo | 96,18% | 95,09% | 98,45% | 100,00% |
| Quibe | 91,01% | 62,63% | 88,11% | 51,04% |
| Risoles | 99,41% | 98,11% | 100,00% | 98,11% |
| Sanduíche | 74,31% | 87,43% | 78,11% | 88,66% |
| **Média** | **89,78%** | **90,51%** | **87,55%** | **91,60%** |


### Discussão


O modelo monolabel apresentou convergência rápida e estável, com métricas superiores a 94% (mAP@50:95), refletindo a simplicidade da tarefa unificada. O modelo multilabel mostrou comportamento mais complexo, com desempenho heterogêneo entre classes.


**Alto desempenho:** Risoles (99,41%), Folhado (97,69%), Pão de queijo (96,18%) e Esfiha (94,57%).


**Desempenho inferior:** Quibe apresentou degradação significativa no teste (62,63%), enquanto Coxinha e Bolinha de queijo mostraram baixa precisão na validação, melhorando no teste.


As oscilações nas curvas de treinamento multilabel refletem a dificuldade em generalizar entre 14 categorias visualmente similares, evidenciando desafios inerentes à classificação fina de múltiplas classes.
