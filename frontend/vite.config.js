import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { fileURLToPath } from 'url';
import { quasar, transformAssetUrls } from '@quasar/vite-plugin';
import path from 'path'; // Import path module

// https://vitejs.dev/config/
export default defineConfig({
  base: "./",
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  plugins: [
    vue({
      template: { transformAssetUrls },
    }),
    quasar({
      sassVariables: fileURLToPath(new URL('./src/quasar-variables.sass', import.meta.url))
      // sassVariables: 'src/quasar-variables.sass',
    }),
  ]
});

// build: {
//   outDir: 'public', // Change to 'public' directory
// },
// resolve: {
//   alias: {
//     "@": path.resolve(__dirname, "./src"), // Correctly set the alias
//   },
// },