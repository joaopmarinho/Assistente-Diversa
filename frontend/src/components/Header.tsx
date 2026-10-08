import type { Perfil } from "../types";

interface Props {
  perfis: Perfil[];
  perfil: string;
  onChange: (nome: string) => void;
}

export function Header({ perfis, perfil, onChange }: Props) {
  return (
    <header className="hero">
      <div style={{display: "flex", flexDirection: "column", alignItems: "start", justifyContent: "space-between", gap: "1rem"}}>
        <h1>
          <img src="/imagens/images.svg" alt="" className="icone-grupo" />
          Acessibilidade Inteligente <span className="detalhe">&gt;</span>
        </h1>
        <p className="descricao">
          Assistente acadêmico para apoio à educação inclusiva, com respostas adaptadas para Professor, Família e Gestor.
        </p>
      </div>

      <div className="perfil" style={{display: "flex", flexDirection: "column", gap: "0.5rem", justifyContent: "center"}}>
        <label htmlFor="perfil">Tipo de usuário</label>
        <select id="perfil" value={perfil} onChange={(e) => onChange(e.target.value)}>
          {perfis.map((p) => (
            <option key={p.nome} value={p.nome}>
              {p.nome}
            </option>
          ))}
        </select>
      </div>
    </header>
  );
}
