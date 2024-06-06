"use client";

import { Button } from '@chakra-ui/react'
import { useRouter } from 'next/navigation';

const ToRegisterButton = () => {
    const router = useRouter("");
    const redirectToRegisterPage = () => {
        router.push("/auth/register");
    }
    return (
        <>
            <Button 
                onClick={redirectToRegisterPage}
                colorScheme="teal"
            >サインアップ</Button>
        </>
    )
}

export default ToRegisterButton;