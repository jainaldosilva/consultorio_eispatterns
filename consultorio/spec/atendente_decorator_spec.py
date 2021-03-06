import unittest
from should_dsl import should, should_not
from eispatterns.domain.node.person import Person
from eispatterns.domain.node.machine import Machine
from consultorio.decorators.atendente_decorator import AtendenteDecorator
from consultorio.decorators.paciente_decorator import PacienteDecorator
from consultorio.decorators.consulta_decorator import ConsultaDecorator
from consultorio.rules.doctors_office_rules_base import DoctorsOfficeRuleBase
from eispatterns.domain.supportive.rule_manager import RuleManager




class AtendenteDecoratorSpec(unittest.TestCase):
    ''' Atendente Decorator Spec '''

    def setUp(self):
        RuleManager.rule_base = DoctorsOfficeRuleBase()
        self.atendente_decorator = AtendenteDecorator("Pedro")
        #test doubles won't work given type checking rules, using classic
        self.pessoa = Person()
        #RuleManager.rule_base = DoctorsOfficeRuleBase

    def test_decorador_uma_pessoa(self):
        #should work
        self.atendente_decorator.decorate(self.pessoa)
        self.atendente_decorator.decorated |should| be(self.pessoa)
        self.atendente_decorator.decorated |should| have(1).decorators
        #should fail
        decorate,_,_ = self.atendente_decorator.decorate('Nao sou uma pessoa')
        decorate |should| equal_to(False)

    def test_generates_register(self):
        self.atendente_decorator.generate_register('44-20202')
        self.atendente_decorator.register |should| equal_to('44-20202')


    def test_solicita_agendamento(self):
        '''solicita agendamento apenas para consultas nao agendadas '''

        pessoa_paciente = Person()
        paciente = PacienteDecorator("Lucas")
        paciente.decorate(pessoa_paciente)

        maquina_consulta = Machine()
        consulta = ConsultaDecorator("0123")
        consulta.decorate(maquina_consulta)
        consulta.set_valor_da_consulta(10)

        self.atendente_decorator.decorate(self.pessoa)

        #consulta ainda nao agendada
        self.atendente_decorator.solicitar_agendamento(consulta, paciente, "20/01/2014")

        self.pessoa.input_area |should| contain("0123")
        paciente.consultas_agendadas["0123"]|should| be(consulta)
        consulta.agendada |should | equal_to(True)

        pessoa_paciente2 = Person()
        paciente2 = PacienteDecorator("Igor")
        paciente2.decorate(pessoa_paciente2)

        #consulta ja foi agendada
        self.atendente_decorator.solicitar_agendamento(consulta, paciente2, "20/01/2014")

        self.pessoa.input_area |should_not| have(2).elements
        paciente2.consultas_agendadas |should_not| include_keys('0123')
