import { useCallback, useEffect, useRef, useState } from "react";

// A tipagem de SpeechRecognition ainda não está no lib.dom do TypeScript.
interface Reconhecimento {
  lang: string;
  interimResults: boolean;
  onresult: ((e: { results: ArrayLike<ArrayLike<{ transcript: string }>> }) => void) | null;
  onend: (() => void) | null;
  onerror: (() => void) | null;
  start(): void;
  stop(): void;
}

type Construtor = new () => Reconhecimento;

const Reconhecedor: Construtor | undefined =
  (window as unknown as { SpeechRecognition?: Construtor; webkitSpeechRecognition?: Construtor })
    .SpeechRecognition ??
  (window as unknown as { webkitSpeechRecognition?: Construtor }).webkitSpeechRecognition;

export function useDitado(aoReconhecer: (texto: string) => void) {
  const [ouvindo, setOuvindo] = useState(false);
  const ref = useRef<Reconhecimento | null>(null);
  const callback = useRef(aoReconhecer);
  callback.current = aoReconhecer;

  const alternar = useCallback(() => {
    if (!Reconhecedor) return;
    if (ref.current) {
      ref.current.stop();
      return;
    }
    const r = new Reconhecedor();
    r.lang = "pt-BR";
    r.interimResults = false;
    r.onresult = (e) => callback.current(e.results[0][0].transcript);
    r.onend = r.onerror = () => {
      ref.current = null;
      setOuvindo(false);
    };
    ref.current = r;
    setOuvindo(true);
    r.start();
  }, []);

  useEffect(() => () => ref.current?.stop(), []);

  return { suportado: Boolean(Reconhecedor), ouvindo, alternar };
}

const suportaFala = "speechSynthesis" in window;

function removerMarkdown(texto: string): string {
  return texto.replace(/[*_`#>]/g, "").replace(/\[([^\]]+)\]\([^)]+\)/g, "$1");
}

export function useLeitura() {
  const [lendo, setLendo] = useState(false);

  const alternar = useCallback((texto: string) => {
    if (!suportaFala) return;
    if (speechSynthesis.speaking) {
      speechSynthesis.cancel();
      setLendo(false);
      return;
    }
    const fala = new SpeechSynthesisUtterance(removerMarkdown(texto));
    fala.lang = "pt-BR";
    fala.onend = fala.onerror = () => setLendo(false);
    setLendo(true);
    speechSynthesis.speak(fala);
  }, []);

  useEffect(() => () => speechSynthesis.cancel(), []);

  return { suportado: suportaFala, lendo, alternar };
}
