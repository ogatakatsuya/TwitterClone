import { cookies } from "next/headers";

import { Flex, Grid, Heading, Input, VStack, Container } from "@chakra-ui/react";
import PostIndex from "./_components/PostIndex";
import PostButton from "./_components/PostButton";
import MenuBar from "./_components/MenuBar"

const Home = () => {
    const access_token = cookies().has("access_token");
    return (
        <Container maxW="1000px" mt="10" centerContent>
            <Grid templateColumns="200px 500px 200px" gap={10} padding={4}>
                <MenuBar />
                <Flex direction="column" align="center">
                    <PostIndex />
                    { access_token && <PostButton />}
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
