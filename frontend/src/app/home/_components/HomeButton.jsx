"use client";

import { useRouter } from "next/navigation";
import { Button } from "@chakra-ui/react"

const HomeButton = () => {
    const router = useRouter()
    const redirectToHome = () => {
        router.push("/home");
    }
    return(
        <Button variant="link" onClick={redirectToHome}>Home</Button>
    )
}

export default HomeButton;