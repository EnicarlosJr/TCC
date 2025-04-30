from django.core.management.base import BaseCommand
from faker import Faker
import random
from datetime import timedelta
from django.utils import timezone

# Importa seus modelos aqui
from paciente.models import (
    Paciente, HistoriaSocial, HabitosAlimentares, PerfilClinico,
    AutonomiaMedicamentos, Saude, Doenca, Medicamento, MedicamentoDoencaPaciente
)
from consulta.models import Consulta, ProblemaSaude, Medicamento as MedicamentoConsulta, Avaliacao, PlanoAtuacao

fake = Faker('pt_BR')

class Command(BaseCommand):
    help = 'Gera pacientes, consultas, problemas de saúde e medicamentos fake'

    def handle(self, *args, **options):
        self.stdout.write('🔄 Iniciando geração de dados fake...')

        self.criar_dados(qtd_pacientes=20)

        self.stdout.write(self.style.SUCCESS('✅ Dados fake gerados com sucesso!'))

    def criar_doencas_e_medicamentos(self, qtd=20):
        if Doenca.objects.count() < qtd:
            for _ in range(qtd - Doenca.objects.count()):
                Doenca.objects.create(nome=fake.unique.word())

        if Medicamento.objects.count() < qtd:
            for _ in range(qtd - Medicamento.objects.count()):
                Medicamento.objects.create(nome=fake.unique.word())

    def criar_dados(self, qtd_pacientes=10):
        self.criar_doencas_e_medicamentos(qtd=20)

        doencas = list(Doenca.objects.all())
        medicamentos = list(Medicamento.objects.all())

        for _ in range(qtd_pacientes):
            paciente = Paciente.objects.create(
                nome=fake.name(),
                telefone=fake.phone_number(),
                responsavel=fake.name(),
                data_nascimento=fake.date_of_birth(minimum_age=18, maximum_age=90),
                genero=random.choice(['M', 'F', 'Outro']),
                estado_civil=random.choice(['Solteiro', 'Casado', 'Viúvo', 'Separado']),
                bairro=fake.bairro(),
                distrito=fake.city_suffix(),
                municipio=fake.city(),
                escolaridade=random.choice(['Fundamental', 'Médio', 'Superior']),
                ocupacao=fake.job(),
                raca=random.choice(['Branco', 'Negro', 'Pardo', 'Indígena', 'Outro']),
                reside_com=random.choice(['Família', 'Sozinho', 'Instituição']),
                observacoes=fake.text(max_nb_chars=200)
            )

            # Historias sociais
            HistoriaSocial.objects.create(
                paciente=paciente,
                consome_bebida=random.choice([True, False]),
                tipos_bebidas=fake.word(),
                quantidade_ingerida=random.randint(1, 5),
                frequencia_uso=random.choice(['Diário', 'Semanal', 'Mensal']),
                fumante=random.choice([True, False]),
                tempo_parou=random.randint(0, 10),
                tempo_fumou=random.randint(1, 30),
                pratica_atividade_fisica=random.choice([True, False]),
                atividades_fisicas=fake.word(),
                frequencia_atividade=random.choice(['Diário', 'Semanal', 'Mensal']),
                observacoes=fake.sentence()
            )

            # Hábitos alimentares
            HabitosAlimentares.objects.create(
                paciente=paciente,
                horario_acorda=fake.time(),
                cafe_da_manha=fake.word(),
                lanche_manha=fake.word(),
                almoco=fake.word(),
                lanche_tarde=fake.word(),
                jantar=fake.word(),
                horario_dorme=fake.time(),
                ultima_refeicao=fake.word(),
                observacoes=fake.sentence()
            )

            # Perfil clínico
            PerfilClinico.objects.create(
                paciente=paciente,
                capacidade_atividade=random.choice(['Total', 'Parcial', 'Nenhuma']),
                incomodo=random.choice([True, False]),
                ultima_visita_dentista=fake.date_between(start_date='-3y', end_date='today'),
                percepcao_saude=random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),  
                observacoes=fake.sentence()
            )

            # Autonomia medicamentosa
            AutonomiaMedicamentos.objects.create(
                paciente=paciente,
                autonomia_gestao=random.choice([True, False]),
                autonomia_outro=fake.name(),
                dificuldade_tomar=random.choice([True, False]),
                dificuldade_outro=fake.word(),
                esquecimentos=random.choice([True, False]),
                toma_no_horario=random.choice([True, False]),
                interrompe_quando_bem=random.choice([True, False]),
                interrompe_quando_mal=random.choice([True, False]),
                desconforto_medicamento=random.choice([True, False]),
                desconforto_outro=fake.sentence(),
                uso_alternativos=random.choice([True, False]),
                uso_alternativos_outro=fake.sentence(),
                local_guarda=random.choice(['Cozinha', 'Banheiro', 'Sala']),
                forma_descarte=random.choice(['Descarta corretamente', 'Lixo comum', 'Outro']),
                forma_descarte_outro=fake.sentence(),
                pressao_arterial=f"{random.randint(10, 14)}x{random.randint(6, 9)}",
                frequencia_cardiaca=f"{random.randint(60, 100)} bpm",
                glicemia=f"{random.randint(70, 150)} mg/dL",
                observacoes_importantes=fake.text(max_nb_chars=120)
            )

            # Saúde geral
            Saude.objects.create(
                paciente=paciente,
                incomodo=random.choice([True, False]),
                informacoes_importantes=fake.text(max_nb_chars=120),
                ultima_visita_dentista=fake.date_between(start_date='-2y', end_date='today'),
                percepcao_saude=random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
                justificativa=fake.sentence(),
                pressao_controlada=random.choice([True, False]),
                observacoes=fake.text(max_nb_chars=120)
            )

            # Relaciona doenças e medicamentos
            for _ in range(random.randint(1, 3)):
                MedicamentoDoencaPaciente.objects.create(
                    paciente=paciente,
                    doenca=random.choice(doencas),
                    medicamento=random.choice(medicamentos),
                    observacao=fake.sentence()
                )

            # Criar 1-3 consultas para o paciente
            for _ in range(random.randint(1, 3)):
                data_consulta = fake.date_between(start_date='-1y', end_date='today')
                consulta = Consulta.objects.create(
                    paciente=paciente,
                    data_consulta=data_consulta,
                    evolucao=fake.paragraph(nb_sentences=5),
                    motivo_consulta=fake.sentence(),
                    prescricoes_exames=fake.sentence(),
                    data_proxima_revisao=fake.date_between(start_date=data_consulta, end_date='+6m')
                )

                problema = ProblemaSaude.objects.create(
                    consulta=consulta,
                    problema=random.choice(doencas).nome,
                    inicio=fake.date_between(start_date='-1y', end_date=data_consulta),
                    controlado=random.choice([True, False]),
                    preocupa=random.choice([True, False])
                )

                medicamento_consulta = MedicamentoConsulta.objects.create(
                    consulta=consulta,
                    nome=random.choice(medicamentos).nome,
                    classe=random.choice(['Analgésico', 'Antibiótico', 'Antidepressivo', 'Anti-hipertensivo']),
                    desde=fake.date_between(start_date='-1y', end_date=data_consulta),
                    prescrita=fake.word(),
                    utilizada=fake.word(),
                    para_que_servir=fake.sentence(),
                    problema_saude=problema
                )

                Avaliacao.objects.create(
                    medicamento=medicamento_consulta,
                    necessidade=random.choice([True, False]),
                    efetividade=random.choice([True, False]),
                    seguranca=random.choice([True, False]),
                    causa_rnm=fake.sentence(),
                    classificacao_rnm_1=random.choice(['Necessidade', 'Segurança', 'Efetividade']),
                    classificacao_rnm_2=random.choice(['Primário', 'Secundário']),
                    situacao_problema_saude=random.choice(['Resolvido', 'Em tratamento', 'Sem alteração'])
                )

                PlanoAtuacao.objects.create(
                    consulta=consulta,
                    objetivos=fake.sentence(),
                    descricao_planejamento=fake.sentence(),
                    resultado=fake.sentence(),
                    data_intervencao=fake.date_between(start_date=data_consulta, end_date='+2m'),
                    data_alcancado=fake.date_between(start_date='today', end_date='+6m'),
                    registro_intervencao=random.choice(['Intervenção Direta', 'Orientação']),
                    classificacao_intervencao=random.choice(['Educacional', 'Farmacológica']),
                    prioridade=random.choice(['Alta', 'Média', 'Baixa'])
                )
