import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: '0.0.0.0',
    allowedHosts: ['f4b652bcecb7.ngrok-free.app'],
    hmr: {
      clientPort: 443
    }
  }
})
