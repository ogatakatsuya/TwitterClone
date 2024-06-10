import { cookies } from "next/headers";

import { Flex, Grid, Heading, Input, VStack, Container } from "@chakra-ui/react";
import PostIndex from "./_components/PostIndex";
import PostButton from "./_components/PostButton";
import MenuBar from "./_components/MenuBar"
import SearchBar from "./_components/SearchBar"

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
                <SearchBar />
            </Grid>
        </Container>
    );
};

export default Home;
