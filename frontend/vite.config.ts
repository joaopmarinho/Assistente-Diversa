import react from "@vitejs/plugin-react";
import { defineConfig, loadEnv } from "vite";

export default defineConfig(({ mode }) => {
  // API_PROXY aponta para o serviço "backend" quando o Vite roda no Docker.
  const env = loadEnv(mode, ".", "");
  return {
    plugins: [react()],
    server: {
      proxy: { "/api": env.API_PROXY || "http://localhost:8000" },
    },
  };
});
