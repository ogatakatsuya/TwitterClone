import { Button } from '@chakra-ui/react'
import { useRouter } from 'next/navigation'

const ToLoginButton = () => {
    const router = useRouter();
    const onClick = () => {
        router.push("/auth/login");
    }
    return (
        <>
            <Button onClick={onClick}>ログイン</Button>
        </>
    )
}

export default ToLoginButton;