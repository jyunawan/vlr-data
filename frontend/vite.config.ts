import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import { tanstackRouter } from "@tanstack/router-plugin/vite";
import path from "path";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    // Please make sure that '@tanstack/router-plugin' is passed before '@vitejs/plugin-react'
    tanstackRouter({
      target: "react",
      autoCodeSplitting: true,
    }),
    react(),
    tailwindcss(),
    // ...,
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
      "@components": path.resolve(__dirname,"src/components"),
      "@utils": path.resolve(__dirname,"src/utils"),
      "@assets": path.resolve(__dirname,"src/assets"),
      "@hooks": path.resolve(__dirname,"src/hooks"),
      "@types": path.resolve(__dirname,"src/types"),
    },
  },
});
