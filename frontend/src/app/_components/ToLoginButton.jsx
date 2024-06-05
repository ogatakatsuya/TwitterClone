import { Button } from '@chakra-ui/react'
import { useRouter } from 'next/navigation'

const ToLoginButton = () => {
    const router = useRouter();
    const redirectToLoginPage = () => {
        router.push("/auth/login");
    }
    return (
        <>
            <Button onClick={redirectToLoginPage}>ログイン</Button>
        </>
    )
}

export default ToLoginButton;