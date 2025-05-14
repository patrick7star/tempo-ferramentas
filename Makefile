PYTHONPATH="$(PATH):./lib/utils"
PYEXEC = "/usr/bin/python3"
VERSAO = iv
NOME = tempo-tools
ARCHIVE = $(NOME)-$(VERSAO).tar

# Algoritmo apenas salva na máquina local de desenvolvimento. Isso, porque
# lá tem o diretório repositório com os códigos versionados.
salva:
	tar -cvf --wildcards --exclude=*pycache* ../versões/$(ARCHIVE) *

debug:
	export PYTHONPATH
	$(PYEXEC) -BO src/main.py

testes = simples_instanciacao atributo_e_criado_em_runtime

$(testes):
	$(PYEXEC) -BO -m unittest src.telinha.CronometroLedUnitarios.$@
