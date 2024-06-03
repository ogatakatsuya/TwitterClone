"use client"

import { Button } from "@chakra-ui/react"
const LogoutButotn = () => {
    const onClick = () => {
        console.log("logout");
    }
    return(
        <>
        <Button
        colorScheme = "red"
        onClick = {onClick}
        >
            ログアウト
        </Button>
        </>
    )
}

export default LogoutButotn;