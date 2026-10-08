from app.services.persona import normalizar_perfil
from app.services.rag import ArtigoEncontrado
from app.services.sugestoes import resposta_garantida, resposta_por_chave
from app.services.text import normalizar

_TDAH = {
    "Professor": (
        "Para trabalhar com alunos com TDAH em sala de aula, o professor pode organizar uma rotina previsível, dividir as atividades em etapas menores e usar instruções claras. Também ajuda combinar pausas curtas, variar estratégias de participação e acompanhar se o estudante compreendeu a tarefa antes de iniciar.\n\n"
        "A inclusão não depende apenas do aluno se adaptar à aula. A escola deve observar quais barreiras dificultam atenção, organização, permanência e participação, articulando professor, AEE e família quando necessário."
    ),
    "Família": (
        "Para apoiar um estudante com TDAH, a família pode conversar com a escola sobre o que ajuda na rotina, na atenção e na organização das atividades. É importante acompanhar se as orientações estão claras, se existem combinados simples e se o estudante recebe apoio sem ser exposto ou rotulado.\n\n"
        "A parceria entre família, professor e AEE ajuda a transformar as necessidades do estudante em estratégias práticas e respeitosas."
    ),
    "Gestor": (
        "Para apoiar alunos com TDAH, a gestão pode orientar a equipe a registrar barreiras de participação, organizar rotinas pedagógicas mais acessíveis e articular professor, AEE e família.\n\n"
        "Também é importante acompanhar práticas de sala, evitar respostas punitivas para dificuldades de atenção e garantir que os apoios estejam previstos no planejamento escolar."
    ),
}

_COM_ARTIGOS = {
    "Professor": (
        "A pergunta está dentro do tema de Educação Inclusiva. Com base nos conteúdos recuperados, a orientação principal é identificar barreiras de participação e aprendizagem, planejar estratégias acessíveis e acompanhar se os apoios estão funcionando na prática.\n\n"
        "O professor pode adaptar a forma de apresentar o conteúdo, diversificar atividades, usar recursos de acessibilidade e dialogar com o AEE para que o estudante participe junto com a turma."
    ),
    "Família": (
        "A pergunta está relacionada à Educação Inclusiva. De forma prática, a família pode buscar diálogo com a escola para entender quais barreiras o estudante enfrenta e quais apoios estão sendo oferecidos.\n\n"
        "O mais importante é acompanhar se a criança ou adolescente participa das atividades com respeito, segurança e oportunidades reais de aprendizagem."
    ),
    "Gestor": (
        "A pergunta está relacionada à Educação Inclusiva. Para a gestão, o ponto central é organizar condições para que a inclusão aconteça de forma planejada, com responsabilidades claras e acompanhamento.\n\n"
        "Isso envolve mapear barreiras, articular professor e AEE, apoiar práticas pedagógicas acessíveis e registrar os apoios necessários para participação e aprendizagem."
    ),
}

_SEM_BASE = (
    "Minha especialidade é Educação Inclusiva. A base atual ainda não encontrou trechos suficientes para essa pergunta, "
    "mas você pode usar as perguntas sugeridas ou perguntar sobre AEE, TEA, TDAH, acessibilidade e inclusão escolar."
)


def resposta_demo(pergunta: str, artigos: list[ArtigoEncontrado], perfil: str) -> str:
    """Resposta local usada quando a Groq não está configurada ou não responde."""
    perfil = normalizar_perfil(perfil)

    garantida = resposta_garantida(pergunta, perfil)
    if garantida:
        return garantida

    base = normalizar(
        " ".join(a.titulo for a in artigos) + " " + " ".join(a.trecho for a in artigos) + " " + pergunta
    )

    if any(t in base for t in ("tdah", "deficit de atencao", "hiperatividade")):
        return _TDAH[perfil]
    if any(t in base for t in ("tea", "autismo", "autista")):
        return resposta_por_chave("como incluir um aluno com tea em sala de aula", perfil)
    if "aee" in base or "atendimento educacional especializado" in base:
        return resposta_por_chave("o que e atendimento educacional especializado", perfil)
    if any(t in base for t in ("educacao inclusiva", "inclusao", "inclusiva")):
        return resposta_por_chave("o que e educacao inclusiva", perfil)
    if artigos:
        return _COM_ARTIGOS[perfil]
    return _SEM_BASE
