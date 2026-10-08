import type { Fonte } from "../types";

interface Props {
  perguntasSugeridas: string[];
  fontes: Fonte[];
  carregando: boolean;
  onPerguntar: (pergunta: string) => void;
}

export function Sidebar({ perguntasSugeridas, fontes, carregando, onPerguntar }: Props) {
  return (
    <aside className="lateral">
      <section className="card">
        <h2>Sugestões de perguntas</h2>
        <div className="sugestoes">
          {perguntasSugeridas.map((p) => (
            <button key={p} type="button" className="botao botao-secundario" disabled={carregando} onClick={() => onPerguntar(p)}>
              {p}
            </button>
          ))}
        </div>
      </section>

      <section className="card">
        <h2>Fontes consultadas</h2>
        {fontes.length === 0 ? (
          <p className="suave">As fontes da última resposta aparecem aqui.</p>
        ) : (
          <ul className="fontes">
            {fontes.map((f) => (
              <li key={f.url}>
                <a href={f.url} target="_blank" rel="noopener noreferrer">
                  {f.titulo}
                </a>
              </li>
            ))}
          </ul>
        )}
      </section>
    </aside>
  );
}
