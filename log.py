__author__ = 'ginezf'
import logging
import logging.config
import os
import sys

class Log:

    def __init__(self, nome_instancia):
        dir = os.getcwd()
        arquivo_conf = os.path.join(dir,'config\\log.conf')
        logging.config.fileConfig(arquivo_conf)
        self.nome = nome_instancia
        # create logging instances
        if nome_instancia == "sensor":
            self.log = logging.getLogger("sensor")
        elif nome_instancia == "features":
            self.log = logging.getLogger("features")
        elif nome_instancia == "svm":
            self.log = logging.getLogger("svm")
        elif nome_instancia == "app":
            self.log = logging.getLogger("app")
        else:
            self.log = logging.getLogger("root")
        pass

    def escreve(self, mensagem, nivel):
        if nivel == logging.CRITICAL:
            self.log.critical(mensagem)
        elif nivel == logging.ERROR:
            self.log.error(mensagem)
        elif nivel == logging.WARNING:
            self.log.warning(mensagem)
        elif nivel == logging.INFO:
            self.log.info(mensagem)
        elif nivel == logging.DEBUG:
            self.log.debug(mensagem)
        elif nivel == logging.NOTSET:
            self.log.debug(mensagem)
        else:
            pass
