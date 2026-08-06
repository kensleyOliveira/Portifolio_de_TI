
import './globals.css'

export const metadata = {
  title: 'Telemetria Agrícola',
  description: 'Monitoramento de microclima',
}

export default function RootLayout({ children }) {
  return (
    // Adicione o idioma correto e o suppressHydrationWarning aqui
    <html lang="pt-BR" suppressHydrationWarning>
      <body>{children}</body>
    </html>
  )
}