import { cookies } from "next/headers";

import { Flex, Grid, Container } from "@chakra-ui/react";
import PostIndex from "./_components/PostIndex";
import MenuBar from "./_components/MenuBar"
import SearchBar from "./_components/SearchBar"

const Home = () => {
    const access_token = cookies().has("access_token");
    return (
        <Container maxW="1000px" mt="10" centerContent>
            <Grid templateColumns="200px 500px 200px" gap={50} padding={4}>
                <MenuBar />
                <Flex direction="column" align="center">
                    <PostIndex />
                </Flex>
                <SearchBar />
            </Grid>
        </Container>
    );
};

export default Home;
