from should_dsl import should, ShouldNotSatisfied
from eispatterns.domain.base.decorator import Decorator
from eispatterns.domain.node.person import Person


class PacienteDecorator(Decorator):
    '''Paciente Decorator'''
    decoration_rules = ['should_be_instance_of_person']

    def __init__(self, nome):
        Decorator.__init__(self)
        self.description = "Supplies the basis for representing Paciente"
        self.name = nome
        self.consultas_agendadas = {}

    def generate_register(self, register):
        ''' generates the register number for the paciente '''
        self.register = register

    def pagar_consulta(self, numero):
        consulta = self.consultas_agendadas[numero]

        if consulta.atendida and not consulta.paga:
            consulta.paga = True
        

