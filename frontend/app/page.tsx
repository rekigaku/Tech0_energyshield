import { Box, Heading, Text, Image } from "@chakra-ui/react";

export default function Home() {
  return (
    <Box p={5}>
      <Heading as="h1" size="xl" mb={4}>Device Information</Heading>
      <Text mb={4}>This is a sample page using Chakra UI and Next.js with TypeScript.</Text>
      <Image src="/images/massage_chair.jpg" alt="Massage Chair" />
    </Box>
  );
}
