import {
    HStack,
    Link,
    Text,
    Flex,
} from "@chakra-ui/react"

const Bar = () => {
    return(
        <>
            <Flex justifyContent="center">
                <HStack spacing="30px">
                    <Link href="#">Posts</Link>
                </HStack>
            </Flex>
        </>
    )
}

export default Bar;