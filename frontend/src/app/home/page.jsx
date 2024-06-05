import { Heading } from "@chakra-ui/react"

import LogoutButton from "./_components/LogoutButton"
import PostIndex from "./_components/PostIndex"
import PostButton from "./_components/PostButton"


const Home = () => {
    return(
        <>
            <PostIndex />
            <LogoutButton />
            <PostButton />
        </>
    )
}

export default Home;