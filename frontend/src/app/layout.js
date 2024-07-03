"use client";

import { CacheProvider } from "@chakra-ui/next-js";
import { ChakraProvider, extendTheme } from "@chakra-ui/react";

const theme = extendTheme({
  // Define your theme settings here
  styles: {
    global: {
      // Global styles
      "html, body": {
        fontFamily: "body",
        lineHeight: "tall",
        color: "gray.700",
        bg: "gray.200",
      },
    },
  },
});

const RootLayout = ({ children }) => {
  return (
    <html lang="en">
      <body>
        <CacheProvider>
          <ChakraProvider theme={theme}>
            {children}
          </ChakraProvider>
        </CacheProvider>
      </body>
    </html>
  )
}

export default RootLayout;