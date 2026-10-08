import type { ChatResponse, Mensagem, PerfisResponse } from "../types";

const BASE = import.meta.env.VITE_API_URL ?? "";

export class ApiError extends Error {
  constructor(
    message: string,
    readonly status: number,
  ) {
    super(message);
  }
}

async function request<T>(caminho: string, init?: RequestInit): Promise<T> {
  let resposta: Response;
  try {
    resposta = await fetch(`${BASE}${caminho}`, init);
  } catch {
    throw new ApiError("Não foi possível conectar ao servidor.", 0);
  }
  if (!resposta.ok) {
    const corpo = await resposta.json().catch(() => null);
    // Sem `detail` a resposta não veio da nossa API (ex.: Lambda desligada ou limitada pela AWS).
    if (corpo?.detail === undefined) throw new ApiError("O serviço está indisponível.", 503);
    throw new ApiError(typeof corpo.detail === "string" ? corpo.detail : "Pergunta inválida.", resposta.status);
  }
  return resposta.json() as Promise<T>;
}

export const buscarPerfis = () => request<PerfisResponse>("/api/profiles");

export const enviarPergunta = (pergunta: string, perfil: string, historico: Mensagem[]) =>
  request<ChatResponse>("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ pergunta, perfil, historico }),
  });
