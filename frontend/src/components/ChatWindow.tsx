import { useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import type { Mensagem } from "../types";

interface Props {
  saudacao: string;
  mensagens: Mensagem[];
  carregando: boolean;
}

export function ChatWindow({ saudacao, mensagens, carregando }: Props) {
  const fim = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fim.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [mensagens, carregando]);

  const todas: Mensagem[] = mensagens.length ? mensagens : [{ role: "assistant", content: saudacao }];

  return (
    <div className="chat" role="log" aria-live="polite" aria-label="Conversa">
      {todas.map((m, i) => (
        <div key={i} className={`bolha bolha-${m.role}`}>
          <ReactMarkdown>{m.content}</ReactMarkdown>
        </div>
      ))}
      {carregando && <div className="bolha bolha-assistant digitando">Pensando…</div>}
      <div ref={fim} />
    </div>
  );
}
