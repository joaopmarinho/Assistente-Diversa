import { useCallback, useEffect, useState } from "react";
import { ApiError, buscarPerfis, enviarPergunta } from "../api/client";
import type { Fonte, Mensagem, PerfisResponse } from "../types";

const CHAVE_STORAGE = "assistente-diversa:conversas";

type PorPerfil<T> = Record<string, T>;

function lerConversas(): PorPerfil<Mensagem[]> {
  try {
    return JSON.parse(localStorage.getItem(CHAVE_STORAGE) ?? "{}");
  } catch {
    return {};
  }
}

export function useChat() {
  const [config, setConfig] = useState<PerfisResponse | null>(null);
  const [indisponivel, setIndisponivel] = useState(false);
  const [perfil, setPerfil] = useState("Professor");
  const [conversas, setConversas] = useState<PorPerfil<Mensagem[]>>(lerConversas);
  const [fontes, setFontes] = useState<PorPerfil<Fonte[]>>({});
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);

  const carregarConfig = useCallback(() => {
    setIndisponivel(false);
    buscarPerfis()
      .then(setConfig)
      .catch(() => setIndisponivel(true));
  }, []);

  useEffect(carregarConfig, [carregarConfig]);

  useEffect(() => {
    localStorage.setItem(CHAVE_STORAGE, JSON.stringify(conversas));
  }, [conversas]);

  const mensagens = conversas[perfil] ?? [];

  const enviar = useCallback(
    async (pergunta: string) => {
      const texto = pergunta.trim();
      if (!texto || carregando) return;

      const historico = conversas[perfil] ?? [];
      setErro(null);
      setCarregando(true);
      setConversas((c) => ({ ...c, [perfil]: [...historico, { role: "user", content: texto }] }));

      try {
        const resposta = await enviarPergunta(texto, perfil, historico);
        setConversas((c) => ({
          ...c,
          [perfil]: [...(c[perfil] ?? []), { role: "assistant", content: resposta.resposta }],
        }));
        setFontes((f) => ({ ...f, [perfil]: resposta.fontes }));
      } catch (e) {
        const status = e instanceof ApiError ? e.status : 0;
        if (status === 0 || status >= 500) setIndisponivel(true);
        setErro(e instanceof ApiError ? e.message : "Erro inesperado.");
        // Desfaz a mensagem do usuário para que ele possa reenviar.
        setConversas((c) => ({ ...c, [perfil]: historico }));
      } finally {
        setCarregando(false);
      }
    },
    [carregando, conversas, perfil],
  );

  const limpar = useCallback(() => {
    setConversas((c) => ({ ...c, [perfil]: [] }));
    setFontes((f) => ({ ...f, [perfil]: [] }));
    setErro(null);
  }, [perfil]);

  return {
    config,
    indisponivel,
    perfil,
    setPerfil,
    mensagens,
    fontes: fontes[perfil] ?? [],
    carregando,
    erro,
    enviar,
    limpar,
    tentarNovamente: carregarConfig,
  };
}
