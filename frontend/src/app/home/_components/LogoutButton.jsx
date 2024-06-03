"use client"

import { Button } from "@chakra-ui/react"
import { useRouter } from "next/navigation"

const LogoutButotn = () => {
    const router = useRouter();

    const onClick = () => {
        const Logout = async () => {
            try{
                const res = await fetch("http://localhost:8000/auth/logout", {
                    method: "GET",
                    credentials: "include"
                });
                if(res.ok){
                    const data = await res.json();
                    console.log(data.message);
                    router.push("./auth/login");
                } else {
                    console.error("Error logout.", res.statusText);
                }
            } catch (error){
                console.error("Error logout...", error);
            }
        };

        Logout();
    }
    return(
        <>
        <Button
        colorScheme = "red"
        onClick = {onClick}
        mt="4"
        >
            ログアウト
        </Button>
        </>
    )
}

export default LogoutButotn;