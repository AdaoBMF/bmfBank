from datetime import datetime
import pytz
from random import randint

class ContaCorrente():
    """
    Cria um objeto ContaCorrente para gerenciar as movimentacoes financeiras dos clientes

    Parametros:
    nome (str): Nome do cliente
    cpf (str): CPF do cliente - deve ser inserido no formato: '000.000.000-00'
    ag (str): Codigo da agencia responsavel pela conta do cliente 
    cc (str): Codigo de identificacao da CC do cliente

    Atributos: 
    nome (str): Nome do cliente
    cpf (str): CPF do cliente - deve ser inserido no formato: '000.000.000-00'
    _saldo (int): Saldo atual da conta do cliente
    _limite_max (int): Limite maximo autorizado para o cliente
    _limite (int): Limite atual disponivel na conta do cliente
    ag (str): Codigo da agencia responsavel pela CC do cliente
    cc (str): Codigo de identificacao da CC do cliente
    _historico (list): Lista com os registros de historico de transacoes da CC
    """
    
    @staticmethod
    def _data_hora():
        """
        Gera um registro com data e hora
        
        """
        fuso_Br = pytz.timezone('Brazil/East')
        d_h = datetime.now(fuso_Br)
        return d_h.strftime('%d/%m/%Y %H:%M:%S')

    def __init__(self, nome, cpf, ag, cc):
        """
        Cria um objeto ContaCorrente para gerenciar as movimentacoes financeiras dos clientes

        Parametros:
        nome (str): Nome do cliente
        cpf (str): CPF do cliente - deve ser inserido no formato: '000.000.000-00'
        ag (str): Codigo da agencia responsavel pela conta do cliente 
        cc (str): Codigo de identificacao da CC do cliente
        """
        self.nome = nome
        self.cpf = cpf
        self._saldo = 0
        self._limite_max = 0
        self._limite = 0
        self.ag = ag
        self.cc = cc
        self._historico = []
        self.cartoes = []

    def saldo_cc(self):
        """
        Exibe o status atual da CC do cliente

        Sem parametros necessarios 
        """
        print("""Cliente: {} CC: {}
Saldo: R${:,.2f}
Limite: R${:,.2f}
Limite disponível: R${:,.2f}
Total disponível: R${:,.2f}
        """.format(self.nome, self.cc, self._saldo, self._limite_max, self._limite, (self._saldo + self._limite_max)))

    def extrato_cc(self):
        """
        Exibe o historico de movimentacao da CC

        Sem parametros necessarios

        """
        print('Extrato cc: {}'.format(self.cc))
        for x in self._historico:
            print(str(x).replace("'",''))
    
    def add_limite(self, valor):
        """
        Define o valor maximo do limite autorizado para a CC

        Parametros:
        valor (int): valor do limite a ser autorizado para esta CC

        """
        
        dif_limite = (valor - self._limite_max)
        self._limite += dif_limite
        self._limite_max = valor
        print("""Limite atualizado
Limite total: R${}
Limite disponível: R${}
        """.format(self._limite_max, self._limite))
     
    def deposito_cc(self, valor):
        """
        Realiza a insercao de credito na CC, atualizando o status da mesma

        Parametros: 
        valor (int): valor a  ser creditado na CC
        """
        if self._limite < self._limite_max:
            limite_usado = (self._limite_max - self._limite)
            sobra = valor - limite_usado
            if sobra > 0:
               self._limite = self._limite_max
               self._saldo = sobra
               self._historico.append((f'Deposito: R${valor:,.2f}',f'Saldo: R${self._saldo:,.2f}',f'Data: {self._data_hora()}'))
               print('Depósito efetuado: R${:,.2f}'.format(valor))
               self.saldo_cc()
            else:
                self._limite += valor
                self._saldo += valor
                self._historico.append((f'Deposito: R${valor:,.2f}',f'Saldo: R${self._saldo:,.2f}',f'Data: {self._data_hora()}'))
                print('Depósito efetuado: R${:,.2f}'.format(valor))
                self.saldo_cc()
        else:
            self._saldo += valor
            self._historico.append((f'Deposito: R${valor:,.2f}',f'Saldo: R${self._saldo:,.2f}',f'Data: {self._data_hora()}'))
            print('Depósito efetuado: R${:,.2f}'.format(valor))
            self.saldo_cc()

    def saque_cc(self, valor):
        """
        Realiza a retirada de credito na CC, atualizando o status da mesma

        Parametros:
        valor(int): valor a ser debitado da CC

        """
        operacao = (self._saldo - valor)
        if operacao >= 0:
            self._saldo -= valor
            self._historico.append((f'Saque: -R${valor:,.2f}',f'Saldo: R${self._saldo:,.2f}',f'Data: {self._data_hora()}'))
            print('Saque efetuado: R${:,.2f}'.format(valor))
            self.saldo_cc()
        else:
            if valor <= (self._saldo + self._limite):
                exed = valor - self._saldo
                self._saldo -= valor
                self._limite -= exed
                self._historico.append((f'Saque: -R${valor:,.2f}',f'Saldo: R${self._saldo:,.2f}',f'Data: {self._data_hora()}'))
                print('Saque efetuado: R${:,.2f}'.format(valor))
                self.saldo_cc()
            else:
                print("""Operação negada: Saldo insuficiente
Total disponível: R${:,.2f}
                """.format((self._saldo+self._limite)))

    def ted(self,valor, recebedor):
        """
        Realiza a transferencia de creditos para um segundo objeto: ContaCorrente

        Parametros:
        valor (int): Valor a ser transferido para o objeto: ContaCorrente de destino
        recebedor (objeto: ContaCorrente): objeto: ContaCorrente que deve receber os creditos transferidos
        """

        operacao = (self._saldo - valor)
        if operacao >= 0:
            self._saldo -= valor
            self._historico.append((f'TED({recebedor.nome}):-{valor:,.2f}',f'Saldo:{self._saldo:,.2f}',f'Data: {self._data_hora()}'))
        else:
            if valor <= (self._saldo + self._limite):
                exed = valor - self._saldo
                self._saldo -= valor
                self._limite -= exed
                self._historico.append((f'TED({recebedor.nome}):-{valor:,.2f}',f'Saldo:{self._saldo:,.2f}',f'Data: {self._data_hora()}'))
            else:
                return print("""Operação negada: Saldo insuficiente
Total disponível: R${:,.2f}
                """.format((self._saldo+self._limite)))
        if recebedor._limite < recebedor._limite_max:
            limite_usado = (recebedor._limite_max - recebedor._limite)
            sobra = valor - limite_usado
            if sobra > 0:
               recebedor._limite = recebedor._limite_max
               recebedor._saldo = sobra
               recebedor._historico.append((f'TED({self.nome}): {valor:,.2f}',f'Saldo:{recebedor._saldo:,.2f}',f'Data: {self._data_hora()}'))
            else:
                recebedor._limite += valor
                recebedor._saldo += valor
                recebedor._historico.append((f'TED({self.nome}): {valor:,.2f}',f'Saldo:{recebedor._saldo:,.2f}',f'Data: {self._data_hora()}'))
        else:
            recebedor._saldo += valor
            recebedor._historico.append((f'TED({self.nome}): {valor:,.2f}',f'Saldo:{recebedor._saldo:,.2f}',f'Data: {self._data_hora()}'))
        print("""Transferência de R${:,.2f} efetuada
Pagador: {}
Recebedor: {}    
            """.format(valor, self.nome, recebedor.nome))


class CartaoCredito:

    """
    Cria um objeto CartaoCredito para gerenciar o uso de credito pelo ciente

    Atributos:
    numero (str): Numero do cartao
    titular (str): Nome do titular do cartao
    validade (str): Data de validade do cartao
    cod_seg (str): codigo de seguranca do cartao
    _limite_max (int): Limite maximo liberado para este cartao
    _limite (int): Limite atual do catrtao
    _senha (str): Senha de liberacao para uso do cartao
    _cc (objeto: ContaCorrente): Conta corrente a que o cartao esta vinculado
    _historico (list): Armazena o historico de uso do cartao
    """

    @staticmethod
    def _data_hora():
        """
        Gera um registro com data e hora
        
        """
        fuso_Br = pytz.timezone('Brazil/East')
        d_h = datetime.now(fuso_Br)
        return d_h.strftime('%d/%m/%Y %H:%M:%S')

    @staticmethod
    def _data_validade():
        """
        Gera um registro com data e hora
        
        """
        fuso_Br = pytz.timezone('Brazil/East')
        d_h = datetime.now(fuso_Br)
        return d_h

    def __init__(self, titular, cc,senha):
        """
        Inicia o cartao

        Parametros:
        titular (str): Nome do titular do cartao
        cc (objeto: ContaCorrente): objeto: ContaCorrente a que o cartao sera vinculado
        senha (str): Senha de utilizacao do cartao
        """
    
        self.numero = str(randint(1000000000000000,9999999999999999))
        self.titular = titular
        self.validade = '{}/{}'.format(CartaoCredito._data_validade().month,CartaoCredito._data_validade().year+4)
        self.cod_seg = '{}{}{}'.format(randint(0,9),randint(0,9),randint(0,9))
        self._limite_max = 1
        self._limite = 1
        self._senha = senha
        self._cc = cc
        self._historico = []
        cc.cartoes.append({self.numero:self})

    def limite_cartao(self, valor):
        """
        Define ao limite do cartao

        Parametros:
        valor (int): valor do novo limite do cartao
        """

        dif_limite = (valor - self._limite_max)
        self._limite += dif_limite	    
        self._limite_max = valor
        print("""Limite atualizado
Limite Total: R${:,.2f}
Limite disponível: R${:,.2f}
    """.format(self._limite_max, self._limite))
    
    def status_cartao(self,senha):
        """
        Exibe o status do cartao

        parameter:
        senha (str): senha de liberacao do usuario - se correta libera a consulta
        """
        if senha == self._senha:
            print("""Limite Total: R${:,.2f}
Limite disponível: R${:,.2f}
        """.format(self._limite_max, self._limite))
        else:
            print('Senha incorreta')

    def uso_cartao(self,valor,id,senha):
        """
        Debita o valor utilizado do limite do cartao

        Parametros:
        valor(int): valor da compra a ser debitada no cartao
        id(str): identificacao do uso ex: 'Compra Magalu' ou 'Boleto Luz'
        senha (str): senha de liberacao do usuario - se correta libera a operacao 
        """

        compra = id
        check = (self._limite-valor)
        if senha==self._senha:
            if check < 0:
                return print("""Operação negada
Motivo: Limite excedido 
Limite disponivel: R${:,.2f}
                """.format(self._limite))
            else:
                self._limite -= valor
                print('compra realizada no valor de R${}'.format(valor))
                self._historico.append((f'{compra} no valor de R${valor:,.2f} ',f'Data: {self._data_hora()}'))
        else:
            print('Senha incorreta')

    def fatura_cartao(self):
        """
        Exibe o hisorico de uso do cartao

        Sem parametros necessarios
        """
        print('Histórico cartão: {} Titular: {} CC: {}'.format(self.numero, self.titular, self._cc.cc))
        for x in self._historico:
            print(str(x).replace("'",''))
        print('-'*30+'fim da fatura'+'-'*30)

    @property
    def senha(self):
        return self._senha
    
    @senha.setter
    def senha(self, password):
        if len(password)==4 and password.isnumeric():
            self._senha = password
        else:
            print("""Senha invalida!!
Insira uma senha numérica de 4 dígitos
            """)


# ------------------------------------------------------------------------------------------------------------------------------------------
# programa

cc_adao = ContaCorrente('Adão Vieira', '965.962.267-54', '123','76214' )
cc_carin = ContaCorrente('Cárin D Trisch','524.687.542-45','123', '76214')
visa_adao = CartaoCredito('Adão Vieira',cc_adao,'5525')
cc_adao.deposito_cc(10000)
cc_adao.ted(500,cc_carin)
visa_adao.limite_cartao(5000)
visa_adao.status_cartao('5525')
visa_adao.uso_cartao(3500,'compra notbook','5525')
visa_adao.fatura_cartao()
visa_adao.status_cartao('5525')
cc_adao.saldo_cc()

