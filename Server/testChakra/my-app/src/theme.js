import { extendTheme } from "@chakra-ui/react";

const customTheme = extendTheme({
  colors: {
    brand: {
      darkBlue: "#2F3B69",
      brown: "#5C4E4E",
      aqua: "#3E829A",
      beige: "#E3DDDC",
    },
  },
  fonts: {
    heading: "Outfit, sans-serif",
    body: "Outfit, sans-serif",
  },
  styles: {
    global: {
      body: {
        bg: "brand.beige",
        color: "brand.darkBlue",
      },
    },
  },
});

export default customTheme;
