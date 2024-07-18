"use client"

import { Button } from "@chakra-ui/react"
import { useRouter } from "next/navigation"

const LogoutButton = () => {
    const router = useRouter();

    const onClick = async () => {
        try{
            const endpointUrl= process.env.NEXT_PUBLIC_BACKEND_ENDPOINT_URL
            const res = await fetch(`${endpointUrl}/auth/logout`, {
                method: "DELETE",
                credentials: "include"
            });
            if(res.ok){
                const data = await res.json();
                router.push("/auth/login");
            } else {
                console.error("Error logout.", res.statusText);
            }
        } catch (error){
            console.error("Error logout...", error);
        }
    }
    return(
        <>
        <Button
        colorScheme = "blackAlpha"
        onClick = {onClick}
        mt="4"
        >
            ログアウト
        </Button>
        </>
    )
}

export default LogoutButton;