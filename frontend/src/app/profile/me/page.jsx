import {
    Container,
    Grid,
    Stack,
    StackDivider
} from "@chakra-ui/react";
import MenuBar from "../../home/_components/MenuBar";
import MyProfileInfo from "./_components/MyProfileInfo"
import MyPost from "./_components/MyPost"
import Bar from "../[user_id]/_components/Bar"


const Profile = () => {
    return(
        <>
        <Container maxW="1000px" mt="10" centerContent>
            <Grid templateColumns="200px 1fr" gap={50} padding={4}>
                <MenuBar />
                <Stack divider={<StackDivider />} spacing='4'>
                    <MyProfileInfo/>
                    <Bar />
                    <MyPost/>
                </Stack>
            </Grid>
        </Container>
        </>
    )
}

export default Profile;