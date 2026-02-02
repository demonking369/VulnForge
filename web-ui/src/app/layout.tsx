import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import '@/styles/globals.css';
import { TopCommandBar } from '@/components/layout/TopCommandBar';
import { LeftNav } from '@/components/layout/LeftNav';
import { StatusStrip } from '@/components/layout/StatusStrip';
import { ChatWidget } from '@/components/chat/ChatWidget';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
    title: 'NeuroRift - Security Intelligence Workspace',
    description: 'A persistent multi-agent security workspace by demonking369',
};

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en" suppressHydrationWarning>
            <body className={inter.className}>
                <div className="h-screen flex flex-col">
                    <TopCommandBar />

                    <div className="flex-1 flex overflow-hidden">
                        <LeftNav />

                        <main className="flex-1 overflow-auto">
                            {children}
                        </main>
                    </div>

                    <StatusStrip />
                    <ChatWidget />
                </div>
            </body>
        </html>
    );
}
