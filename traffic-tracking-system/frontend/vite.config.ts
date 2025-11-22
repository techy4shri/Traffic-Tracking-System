
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import { fileURLToPath } from 'url'

// compute __dirname in ESM
const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

// Vite config with aliases that match tsconfig paths
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: [
      { find: '@', replacement: path.resolve(__dirname, 'src') },
      { find: '@components', replacement: path.resolve(__dirname, 'src/components') },
      { find: '@utils', replacement: path.resolve(__dirname, 'src/utils') },
      { find: '@assets', replacement: path.resolve(__dirname, 'src/assets') },
      { find: '@shared-types', replacement: path.resolve(__dirname, 'src/types') }
    ]
  }
})
