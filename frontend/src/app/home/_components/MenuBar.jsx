import {
    VStack,
    Button,
    Heading,
} from "@chakra-ui/react";
import { cookies } from "next/headers";
import ToLoginButton from "../../_components/ToLoginButton";
import ToRegisterButton from "../../_components/ToRegisterButton";

import LogoutButton from "./LogoutButton";

const MenuBar = () => {
    const access_token = cookies().has("access_token");
    return (
        <>
            {access_token ? 
            (
            <VStack align="center" spacing={4}>
                <Heading as="h2" size="md">Menu</Heading>
                <Button variant="link">Home</Button>
                <Button variant="link">Explore</Button>
                <Button variant="link">Profile</Button>
                <LogoutButton />
            </VStack>
            ):
            (
            <VStack align="start" spacing={4}>
                <Heading as="h2" size="md">Menu</Heading>
                <Button variant="link">Home</Button>
                <Button variant="link">Explore</Button>
                <ToLoginButton/>
                <ToRegisterButton/>
            </VStack>
            )}
        </>
    )
}

export default MenuBar;