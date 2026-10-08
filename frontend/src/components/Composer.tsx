import { useState } from "react";
import { useDitado, useLeitura } from "../hooks/useSpeech";

interface Props {
  carregando: boolean;
  ultimaResposta: string | undefined;
  onEnviar: (texto: string) => void;
  onLimpar: () => void;
}

export function Composer({ carregando, ultimaResposta, onEnviar, onLimpar }: Props) {
  const [texto, setTexto] = useState("");
  const ditado = useDitado((falado) => setTexto((t) => (t ? `${t} ${falado}` : falado)));
  const leitura = useLeitura();

  const enviar = () => {
    if (!texto.trim() || carregando) return;
    onEnviar(texto);
    setTexto("");
  };

  return (
    <div className="composer">
      {leitura.suportado && (
        <button
          type="button"
          className="botao botao-secundario"
          disabled={!ultimaResposta}
          onClick={() => ultimaResposta && leitura.alternar(ultimaResposta)}
        >
          {leitura.lendo ? "⏹ Parar leitura" : "🔊 Ouvir resposta"}
        </button>
      )}

      <div className="campo">
        <textarea
          value={texto}
          rows={3}
          maxLength={1000}
          placeholder="Digite ou fale sua pergunta sobre educação inclusiva…"
          aria-label="Pergunta sobre educação inclusiva"
          onChange={(e) => setTexto(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              enviar();
            }
          }}
        />
        {ditado.suportado && (
          <button
            type="button"
            className={`botao-voz${ditado.ouvindo ? " ativo" : ""}`}
            aria-label={ditado.ouvindo ? "Parar ditado" : "Ditar pergunta por voz"}
            onClick={ditado.alternar}
          >
            🎙️
          </button>
        )}
      </div>

      <div className="linha-botoes">
        <button type="button" className="botao botao-principal" disabled={carregando || !texto.trim()} onClick={enviar}>
          Enviar pergunta
        </button>
        <button type="button" className="botao botao-principal" onClick={onLimpar}>
          Limpar histórico
        </button>
      </div>
    </div>
  );
}
