import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
import tflite_runtime.interpreter as tflite

class Preprocessamento:
    

    # Recorte centralizado na imagem
    def corte_central(self, img, dimension=()):
        # Dimensões da imagem
        width = img.shape[1]
        height = img.shape[0]
        
        # Dimensões da área de recorte
        cut_height = dimension[0]
        cut_width = dimension[1]
        
        # Obtendo as coordenadas para centralizar a área recortada 
        y = (height - cut_height) // 2
        x = (width - cut_width) // 2
        
        # Recorte
        img_cut = img[y:y+cut_height, x:x+cut_width]
        return img_cut


    # Encontrando pixels com valor iguais ao especificado na imagem e recortando
    def cut_digit_region(self, img, pixel_value, margin=10):
        # Retorna as coordenadas onde o valor é igual ao de pixel_value
        points = np.argwhere(img == pixel_value)
        points = np.fliplr(points)
        x, y, w, h = cv2.boundingRect(points)

        # Desconbrindo o maior lado para transformar a área de recorte em um quadrado
        if w > h:
            # y recebe nova coordenada para manter a região de recorte centralizada
            y = y - ((w - h) // 2)

            # Altura recebe o valor da largura
            h = w
        else:
            # x recebe nova coordenada para manter a região de recorte centralizada
            x = x - ((h - w) // 2)

            # Largura recebe o valor da altura
            w = h

        # Acrescentando margem à imagem
        x = x - margin
        y = y - margin
        w = w + (margin * 2)
        h = h + (margin * 2)

        # Verificando se as coordenadas respeitam os limites da imagem
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if (x + w) > img.shape[1]:
            x = img.shape[1] - w
        if (y + h) > img.shape[0]:
            y = img.shape[0] - h

        # Cortando
        img_cropped = img[y:y+h, x:x+w]
        return img_cropped


    def processar(self, img):
        # 1 - Recorte da área de interesse
        largura = img.shape[1] // 2
        altura = img.shape[0] // 2
        img_roi = self.corte_central(img, (altura, largura))
        
        # 2 - Borramento Gaussiano para atenuar o ruído da imagem
        img_gaussian_filter = cv2.GaussianBlur(img_roi, (7, 7), 0)

        # 3 - Aplicando limiar
        img_thresholded = cv2.adaptiveThreshold(img_gaussian_filter, 255,
                                                cv2.ADAPTIVE_THRESH_MEAN_C,
                                                cv2.THRESH_BINARY_INV, 41, 5)

        # 4 - Recorte retangular na região do papel na imagem
        paper_region = self.cut_digit_region(img_thresholded, 255, -150)

        # 5 - Opening, erosão seguido de dilatação (para remocão de artefatos e ruído)
        kernel = np.ones((4, 4), np.uint8)
        opening = cv2.morphologyEx(paper_region, cv2.MORPH_OPEN, kernel)

        # 6 - Dilatação
        kernel = np.ones((5, 5), np.uint8)
        opening = cv2.dilate(opening, kernel, iterations = 1)

        # 7 - Corte do dígito
        cropped_digit_image = self.cut_digit_region(opening, 255, 15)

        # TODO: Procurar outra forma de implementar o anti-aliasing
        # 8 - Borramento Gaussiano para suavizar as bordas do dígito
        cropped_digit_image_inverted = cv2.GaussianBlur(cropped_digit_image, (5, 5), 0)

        # 9 - Redimensionando a imagem e convertendo para np.array
        img_resized = cv2.resize(cropped_digit_image_inverted, (28, 28), cv2.INTER_LINEAR)
        img_reshaped = img_resized.reshape((28, 28))
        img_np_array = np.array(img_reshaped)
        return img_np_array


    # Expandir as dimensões da imagem pre-processada
    def expandir_dims(self, img):
        #image = cv2.resize(img (28,28)).astype("float32")
        img_expanded = np.expand_dims(img, axis=0)
        img_expanded2 = np.expand_dims(img_expanded, axis=img_expanded.ndim)
        return img_expanded2


    # Importando o dataset e colocando em listas
    def importar_dataset(self, path):
        lista_nome_pastas = sorted(os.listdir(path))
        lista_imagens = list()
        print("chegou")
        for i, digito in enumerate(lista_nome_pastas):
            path_pasta_digito = path + digito + '/'
            lista_nome_arquivos = os.listdir(path_pasta_digito)
            print(digito)
            lista_imagens.append(list())
            for nome_arquivo in lista_nome_arquivos:
                img = cv2.imread(path_pasta_digito + nome_arquivo, cv2.IMREAD_GRAYSCALE)
                lista_imagens[i].append(img)
        print("terminou a importação")
        return lista_imagens


    def processarImg(self, imagem):
        img_processada = self.processar(imagem)
        return img_processada

    # Processando as imagens importadas pela função acima
    def processar_imagens_importadas(self, imgs_importadas):
        lista_imgs_processadas = list()
        print("começou a processar")
        for lista_digito_img in imgs_importadas:
            lista_digito_processado = list()
            for imagem in lista_digito_img:
                img_processed = self.processar(imagem)
                lista_digito_processado.append(img_processed)
            lista_imgs_processadas.append(lista_digito_processado)
        print("terminou o processamento")
        return lista_imgs_processadas


    def classificar(self, lista_imgs):
        # Classificando os dígitos processados
        print("começou a classificação")
        
        interpreter = tflite.Interpreter("model.tflite")#importa o modelo model.tflite
        interpreter.allocate_tensors()#aloca tensores para otimizar a inferencia

        input_details = interpreter.get_input_details() #retorna os detalhes de entrada
        output_details = interpreter.get_output_details() #retorna os detalhes de saida

        #interpreter.set_tensor(input_details[0]["index"], img_expanded2)#define o interpretador para ler a imagem
        #interpreter.invoke()#garante que as configurações foram confirmadas
        #pred = interpreter.get_tensor(output_details[0]['index']) #retorna a predição da IA
            
        with open("labels.txt") as f:     #abre o arquivo com os números
            abels = f.read().splitlines()#a serem identificados

        #i = int(np.argmax(pred))
        #label = labels[i]#retorna o numero da predição

        #display.numero(int(label))#mostra o numero no display
        
        total_imgs = 0
        acertos = 0
        acuracia_por_digito = list()
        qtd_imgs_por_digito = list()
        results = np.array([])
        for digito, lista_digito in enumerate(lista_imgs):
            total_imgs += len(lista_digito)
            qtd_imgs_por_digito.append(len(lista_digito))
            acertos_por_digito = 0
            for img_processada in lista_digito:
                img_expanded = self.expandir_dims(img_processada)
                interpreter.set_tensor(input_details[0]["index"], img_expanded)
                interpreter.invoke()
                
                array_predicoes = interpreter.get_tensor(output_details[0]['index'])
                
                #define o interpretador para ler a imagem
                interpreter.invoke()#garante que as configurações foram confirmadas
                predicao = np.argmax(array_predicoes)
                print("--"+str(digito)+"--"+str(predicao)+"--")
                if predicao == digito:
                    acertos += 1
                    acertos_por_digito += 1
            acuracia_por_digito.append(acertos_por_digito)

        variaveis = ['Digito', 'Número de imagens','Acertos', 'Acurácia']
        cabecalho = ' | '.join(variaveis)
        tam = list()
        for val in variaveis:
            tam.append(len(val))

        print(cabecalho)
        for digito, acuracia in enumerate(acuracia_por_digito):
            valores = list()
            valores.append(f'{digito}'.center(tam[0]))
            valores.append(f'{qtd_imgs_por_digito[digito]}'.center(tam[1]))
            valores.append(f'{acuracia_por_digito[digito]}'.center(tam[2]))
            valores.append(f'{(acuracia_por_digito[digito] / qtd_imgs_por_digito[digito]) * 100:.2f}%'.rjust(tam[3]))
            linha = '   '.join(valores)
            print(linha)
        print('-' * len(cabecalho))
        print(f'Total de imagens: {total_imgs}')
        print(f'Acertos: {acertos}')
        print(f'Acurácia: {(acertos / total_imgs) * 100:.2f}%')
