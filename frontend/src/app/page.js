import { Heading } from "@chakra-ui/react"
import ToLoginButton from './_components/ToLoginButton'
import ToRegisterButton from './_components/ToRegisterButton'

export default function Home() {
  return (
    <>
    <Heading>Hello</Heading>
    <ToLoginButton />
    <ToRegisterButton />
    </>
  );
}
