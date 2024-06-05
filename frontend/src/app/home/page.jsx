import { Box, Flex, Grid, Heading, Input, Button, VStack, Container } from "@chakra-ui/react";
import LogoutButton from "./_components/LogoutButton";
import PostIndex from "./_components/PostIndex";
import PostButton from "./_components/PostButton";

const Home = () => {
    return (
        <Container maxW="1000px" mt="10" centerContent>
            <Grid templateColumns="200px 500px 200px" gap={10} padding={4}>
                <VStack align="start" spacing={4}>
                    <Heading as="h2" size="md">Menu</Heading>
                    <Button variant="link">Home</Button>
                    <Button variant="link">Explore</Button>
                    <Button variant="link">Profile</Button>
                    <LogoutButton />
                </VStack>

                <Flex direction="column" align="center">
                    <PostIndex />
                    <PostButton />
                </Flex>

                <VStack align="start" spacing={4} width="100%">
                    <Heading as="h2" size="md">Search</Heading>
                    <Input placeholder="Search posts..." width="100%" />
                </VStack> 
            </Grid>
        </Container>
    );
};

export default Home;
