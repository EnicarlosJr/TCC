import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from paciente.models import Paciente, Doenca, Medicamento as MedicamentoPaciente, MedicamentoDoencaPaciente
from consulta.models import (
    Consulta,
    ProblemaSaude,
    Medicamento as MedicamentoConsulta,
    Avaliacao,
    PlanoAtuacao
)

fake = Faker('pt_BR')


class Command(BaseCommand):
    help = 'Gera pacientes e consultas fictícias para testes'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Iniciando criação de dados fictícios...'))

        # Criar Doenças e Medicamentos de referência
        doencas = ['Diabetes', 'Hipertensão', 'Asma', 'Artrite', 'Depressão']
        medicamentos = ['Metformina', 'Losartana', 'Salbutamol', 'Ibuprofeno', 'Sertralina']

        doenca_objs = [Doenca.objects.get_or_create(nome=d)[0] for d in doencas]
        medicamento_objs = [MedicamentoPaciente.objects.get_or_create(nome=m)[0] for m in medicamentos]

        for _ in range(20):  # Número de Pacientes
            paciente = Paciente.objects.create(
                nome=fake.name(),
                telefone=fake.phone_number(),
                numero_formulario=fake.random_number(digits=6),
                responsavel=fake.name(),
                data_nascimento=fake.date_of_birth(minimum_age=18, maximum_age=90),
                genero=random.choice(['M', 'F', 'O', 'ND']),
                estado_civil=random.choice(['Casado(a)', 'Solteiro(a)', 'Separado(a)', 'Amigado(a)', 'Outro']),
                bairro=fake.street_name(),
                distrito=random.choice(['Rural', 'Urbano']),
                municipio=fake.city(),
                escolaridade=random.choice([
                    'Fundamental completo', 'Médio completo', 'Superior incompleto', 'Superior completo'
                ]),
                ocupacao=fake.job(),
                raca=random.choice(['Pardo', 'Branco', 'Negro', 'Outro']),
                reside_com=fake.first_name(),
                observacoes=fake.sentence(),
            )

            # Associar Doenças e Medicamentos (Paciente)
            doenca = random.choice(doenca_objs)
            medicamento = random.choice(medicamento_objs)
            MedicamentoDoencaPaciente.objects.create(
                paciente=paciente,
                medicamento=medicamento,
                doenca=doenca,
                observacao="Medicação inicial"
            )

            # Criar 1 a 3 Consultas por Paciente
            for _ in range(random.randint(1, 3)):
                consulta = Consulta.objects.create(
                    paciente=paciente,
                    data_consulta=fake.date_between(start_date='-2y', end_date='today'),
                    evolucao=fake.paragraph(nb_sentences=3),
                    motivo_consulta=fake.sentence(),
                    prescricoes_exames=fake.sentence(),
                    data_proxima_revisao=fake.date_between(start_date='today', end_date='+1y')
                )

                # Criar Problemas de Saúde para a Consulta
                for _ in range(random.randint(1, 2)):
                    problema = ProblemaSaude.objects.create(
                        consulta=consulta,
                        problema=random.choice(['Dor nas costas', 'Pressão Alta', 'Falta de ar', 'Depressão', 'Dor articular']),
                        inicio=fake.date_between(start_date='-5y', end_date='today'),
                        controlado=random.choice([True, False]),
                        preocupa=random.choice([True, False])
                    )

                    # Criar Medicamento para cada problema de saúde
                    medicamento_consulta = MedicamentoConsulta.objects.create(
                        consulta=consulta,
                        problema_saude=problema,
                        nome=fake.word().capitalize(),
                        classe=random.choice(['Antibiótico', 'Anti-inflamatório', 'Ansiolítico', 'Hipoglicemiante']),
                        desde=fake.date_between(start_date='-3y', end_date='today'),
                        prescrita=random.choice(['Sim', 'Não']),
                        utilizada=random.choice(['Sim', 'Não']),
                        para_que_servir=fake.sentence(),
                    )

                    # Criar Avaliação para o Medicamento
                    Avaliacao.objects.create(
                        medicamento=medicamento_consulta,
                        necessidade=random.choice([True, False]),
                        efetividade=random.choice([True, False]),
                        seguranca=random.choice([True, False]),
                        classificacao_rnm_1=random.choice(['PSNT', 'EMD', 'INQ', 'IQ', 'ISQ']),
                        classificacao_rnm_2=random.choice(['PSNT', 'EMD', 'INQ', 'IQ', 'ISQ', 'NC']),
                        situacao_problema_saude=random.choice(['PM', 'RA']),
                        causa_rnm=fake.sentence(),
                    )

                # Criar Plano de Ação
                PlanoAtuacao.objects.create(
                    consulta=consulta,
                    objetivos=fake.paragraph(nb_sentences=2),
                    prioridade=random.choice(['baixa', 'media', 'alta']),
                    registro_intervencao=random.choice(['quantidade_medicamento', 'educacao_paciente', 'estrategia_farmacologica']),
                    classificacao_intervencao=random.choice([
                        'modificar_dose', 'adicionar_medicamento', 'substituir_medicamento', 'educar_nao_farmacologico'
                    ]),
                    descricao_planejamento=fake.sentence(),
                    data_intervencao=fake.date_between(start_date='today', end_date='+6m'),
                    alcancado=random.choice([True, False]),
                    data_alcancado=fake.date_between(start_date='today', end_date='+1y') if random.choice([True, False]) else None,
                    resultado=fake.sentence(),
                    rnm_resolvido=random.choice([True, False]),
                    o_que_aconteceu=fake.paragraph(nb_sentences=2)
                )

        self.stdout.write(self.style.SUCCESS('✅ Dados fictícios criados com sucesso!'))
