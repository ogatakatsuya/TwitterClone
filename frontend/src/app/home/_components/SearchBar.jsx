import { VStack, Heading, Input } from "@chakra-ui/react"

const SearchBar = () => {
    return (
        <>
            <VStack align="start" spacing={4} width="100%">
                <Heading as="h2" size="md">Search</Heading>
                <Input placeholder="Search posts..." width="100%" />
            </VStack> 
        </>
    )
}

export default SearchBar;