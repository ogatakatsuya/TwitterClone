import {
    Container,
    Grid,
    Stack,
    StackDivider
} from "@chakra-ui/react";
import MenuBar from "../../home/_components/MenuBar";
import SearchBar from "../../home/_components/SearchBar";
import ProfileInfo from "./_components/ProfileInfo"
import Post from "./_components/Post"
import Bar from "./_components/Bar";

const Profile = ({ params }) => {
    return(
        <>
        <Container maxW="1000px" mt="10" centerContent>
            <Grid templateColumns="200px 1fr" gap={50} padding={4}>
                <MenuBar />
                <Stack divider={<StackDivider />} spacing='4'>
                    <ProfileInfo />
                    <Bar />
                    <Post />
                </Stack>
            </Grid>
        </Container>
        </>
    )
}

export default Profile;