import { useDisclosure, Stack, StackDivider, Container, Grid } from "@chakra-ui/react"

import CommentModal from '../../home/_components/CommentModal';
import Post from "./_components/Post"
import Replies from "./_components/Replies"
import MenuBar from "../../home/_components/MenuBar";
import SearchBar from "../../home/_components/SearchBar";

const postDetail = ({ params }) => {
    
    return(
        <>
        <Container maxW="1000px" mt="10" centerContent>
            <Grid templateColumns="200px 500px 200px" gap={10} padding={4}>
                <MenuBar />
                <Stack divider={<StackDivider />} spacing='4'>
                    <Post post_id={params.post_id}/>
                    <Replies post_id={params.post_id} />
                </Stack>
                <SearchBar />
            </Grid>
        </Container>
        </>
    )
}

export default postDetail;