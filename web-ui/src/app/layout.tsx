import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
    title: 'NeuroRift — Web Mode',
    description: 'AI-powered cybersecurity control plane',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
    return (
        <html lang="en">
            <body className="min-h-screen bg-neuro-bg antialiased">
                {children}
            </body>
        </html>
    );
}
