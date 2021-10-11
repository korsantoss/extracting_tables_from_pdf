# Desafio - Extração de tabelas de um pdf
# by Kaique Oliveira

# para a extração das tabelas do pdf, foi utilizada a biblioteca camelot.
# como instalar:
#!pip install "camelot-py"[cv]

# o camelot possui como dependencia o ghostscript
# caso não esteja instalada, execute:
#!apt install ghostscript python3-tk

# importaçoes necessarias
import camelot
import os
import zipfile
import requests

# diretorio onde os arquivos irao ficar (pdfs, csvs e zip)
directory_files = '/content/'

# declaração dos nomes e caminhos dos arquivos que iremos manipular
file_name_pdf = 'Padrão_TISS_Componente_Organizacional.pdf'
file_name_zip = 'Teste_Intuitive_Care_Kaique_Oliveira.zip'
path_pdf = directory_files+file_name_pdf
path_zip = directory_files+file_name_zip

# verifica se o arquivo .pdf existe. Caso não exista, sera feito o download
check_pdf = os.path.isfile(path_pdf)
if not check_pdf:
  url = 'https://www.gov.br/ans/pt-br/arquivos/assuntos/prestadores/padrao-para-troca-de-informacao-de-saude-suplementar-tiss/padrao-tiss/padrao_tiss_componente_organizacional_202108.pdf'
  resp = requests.get(url)
  with open(path_pdf, 'wb') as file:
    file.write(resp.content)

# verifica se o arquivo zip ja existe. Caso não exista, sera criado.
check_zip = os.path.isfile(path_zip)
if not check_zip:
  tables = camelot.read_pdf(path_pdf, pages='108-114') # realiza a leitura e mapeia as tabelas no pdf
  tables.export(directory_files+'table.csv', f='csv') # exporta as tabelas encontradas e armazena em um caminho
  file_zip = zipfile.ZipFile('Teste_Intuitive_Care_Kaique_Oliveira.zip', 'w') # cria e abre o zip no modo escrita
  
  for file in os.listdir(directory_files): # os.listdir lista tudo do diretorio. Apos listagem, percorremos por eles.
    if file.endswith('.csv'): # caso o arquivo termine com .csv entraremos no if
      file_zip.write(file) # realiza a escrita do arquivo csv no zip
      os.remove(file) # remove o arquivo csv que ja foi escrito no zip 
  file_zip.close()