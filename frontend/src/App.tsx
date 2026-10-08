import { ChatWindow } from "./components/ChatWindow";
import { Composer } from "./components/Composer";
import { Header } from "./components/Header";
import { Sidebar } from "./components/Sidebar";
import { useChat } from "./hooks/useChat";

export default function App() {
  const chat = useChat();

  if (!chat.config) {
    return (
      <main className="pagina estado-vazio">
        {chat.indisponivel ? (
          <>
            <p>O serviço está indisponível no momento.</p>
            <button type="button" className="botao botao-principal" onClick={chat.tentarNovamente}>
              Tentar novamente
            </button>
          </>
        ) : (
          <p>Carregando…</p>
        )}
      </main>
    );
  }

  const perfilAtual = chat.config.perfis.find((p) => p.nome === chat.perfil) ?? chat.config.perfis[0];
  const ultimaResposta = [...chat.mensagens].reverse().find((m) => m.role === "assistant")?.content;

  return (
    <main className="pagina">
      <Header perfis={chat.config.perfis} perfil={chat.perfil} onChange={chat.setPerfil} />

      {chat.indisponivel && (
        <div className="alerta" role="alert">
          O serviço está instável ou indisponível. Tente novamente em instantes.
        </div>
      )}

      <div className="principal">
        <section className="coluna-chat">
          <ChatWindow saudacao={perfilAtual.saudacao} mensagens={chat.mensagens} carregando={chat.carregando} />
          {chat.erro && (
            <div className="alerta" role="alert">
              {chat.erro}
            </div>
          )}
          <Composer
            carregando={chat.carregando}
            ultimaResposta={ultimaResposta}
            onEnviar={chat.enviar}
            onLimpar={chat.limpar}
          />
        </section>

        <Sidebar
          perguntasSugeridas={chat.config.perguntas_sugeridas}
          fontes={chat.fontes}
          carregando={chat.carregando}
          onPerguntar={chat.enviar}
        />
      </div>
    </main>
  );
}
