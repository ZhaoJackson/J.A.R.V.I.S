import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' })

export const metadata: Metadata = {
  title: 'J.A.R.V.I.S - Your Personal Life Assistant',
  description: 'A comprehensive personal web application that integrates various aspects of your life into a single, intelligent interface.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${inter.variable} font-sans bg-gray-50`}>
        <main className="min-h-screen">
          {children}
        </main>
      </body>
    </html>
  )
} 