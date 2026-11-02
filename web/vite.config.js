import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  optimizeDeps: { include: ['cytoscape-cose-bilkent', 'cytoscape', 'graphlib', 'bin-pack', '@neo4j-bloom/dagre'], exclude: ['@neo4j-nvl/layout-workers'] },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
