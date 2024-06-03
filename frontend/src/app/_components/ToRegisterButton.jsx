import { Button } from '@chakra-ui/react'
import { useRouter } from 'next/navigation'

const ToRegisterButton = () => {
    const router = useRouter();
    const onClick = () => {
        router.push("/auth/register");
    }
    return (
        <>
            <Button onClick={onClick}>サインアップ</Button>
        </>
    )
}

export default ToRegisterButton;