import type { Metadata } from 'next';
import { Inter, Outfit } from 'next/font/google';
import '../styles/globals.css';

const inter = Inter({
    subsets: ['latin'],
    variable: '--font-body',
    display: 'swap',
});

const outfit = Outfit({
    subsets: ['latin'],
    variable: '--font-heading',
    display: 'swap',
});

export const metadata: Metadata = {
    title: 'TODOAI | Premium AI-Native Productivity',
    description: 'Experience the extreme level of productivity with our AI-native todo application.',
};

import { Providers } from './providers';

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en" className={`${inter.variable} ${outfit.variable}`}>
            <body className="font-body bg-black text-white antialiased overflow-x-hidden">
                <Providers>{children}</Providers>
            </body>
        </html>
    );
}
