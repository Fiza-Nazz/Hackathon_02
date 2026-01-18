import type { AppProps } from 'next/app';
import { Inter, Outfit } from 'next/font/google';
import '../styles/globals.css';

const inter = Inter({
    subsets: ['latin'],
    variable: '--font-body',
});

const outfit = Outfit({
    subsets: ['latin'],
    variable: '--font-heading',
});

function MyApp({ Component, pageProps }: AppProps) {
    return (
        <div className={`${inter.variable} ${outfit.variable} font-body bg-black`}>
            <Component {...pageProps} />
        </div>
    );
}

export default MyApp;
