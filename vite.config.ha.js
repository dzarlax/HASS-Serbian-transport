import { defineConfig } from 'vite';
import { baseConfig } from './vite.config.base';
import react from '@vitejs/plugin-react';

const isHACS = process.env.HACS === 'true';
const base = isHACS ? '/local/community/beograd_transport/' : '/';

export default defineConfig({
  ...baseConfig,
  base: '/local/community/beograd_transport/',
  plugins: [react()],
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    rollupOptions: {
      input: {
          'dashboard': 'src/client/dashboard.jsx'  // Input stays the same
      },
      output: {
          entryFileNames: 'dashboard.js',  // Changed output filename
      },
    },
    sourcemap: true,
    minify: 'esbuild',
  },
  define: {
    'process.env.NODE_ENV': JSON.stringify('production'),
    'process.env.PUBLIC_URL': JSON.stringify(base),
  },
});