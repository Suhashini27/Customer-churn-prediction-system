import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], weight: ['400', '600'] });

export const metadata: Metadata = {
  title: "Churn Analytics",
  description: "Customer Churn Prediction Dashboard",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-background text-primary min-h-screen`}>
        {children}
      </body>
    </html>
  );
}