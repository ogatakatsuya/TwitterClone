"use client";

import { CacheProvider } from "@chakra-ui/next-js";
import { ChakraProvider } from "@chakra-ui/react";

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <CacheProvider>
          <ChakraProvider>
            {children}
          </ChakraProvider>
        </CacheProvider>
      </body>
    </html>
  )
}