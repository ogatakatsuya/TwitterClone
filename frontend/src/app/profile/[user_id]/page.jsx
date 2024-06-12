import {
    Container,
    Grid,
    Stack,
    StackDivider
} from "@chakra-ui/react";
import MenuBar from "../../home/_components/MenuBar";
import SearchBar from "../../home/_components/SearchBar";

const Profile = ({ params }) => {
    return(
        <>
        <Container maxW="1000px" mt="10" centerContent>
            <Grid templateColumns="200px 500px 200px" gap={50} padding={4}>
                <MenuBar />
                <Stack divider={<StackDivider />} spacing='4'>
                    <h1>{params.user_id}</h1>
                </Stack>
                <SearchBar />
            </Grid>
        </Container>
        </>
    )
}

export default Profile;