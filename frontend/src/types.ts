export type Papel = "user" | "assistant";

export interface Mensagem {
  role: Papel;
  content: string;
}

export interface Fonte {
  titulo: string;
  url: string;
  score: number;
}

export interface Perfil {
  nome: string;
  saudacao: string;
}

export interface PerfisResponse {
  perfis: Perfil[];
  perguntas_sugeridas: string[];
}

export interface ChatResponse {
  resposta: string;
  perfil: string;
  fontes: Fonte[];
  origem: "fora_escopo" | "llm" | "demo" | "garantida";
}
