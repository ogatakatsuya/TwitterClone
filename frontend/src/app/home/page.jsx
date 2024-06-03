import { Heading } from "@chakra-ui/react"

import LogoutButton from "./components/LogoutButton"

const Home = () => {
    return(
        <>
        <Heading>ログインに成功しました！</Heading>
        <LogoutButton />
        </>
    )
}

export default Home;