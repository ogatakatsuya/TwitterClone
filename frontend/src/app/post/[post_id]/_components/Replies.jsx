"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { 
    Card,
    CardBody,
    Text,
    Box,
    Avatar,
    Flex,
    IconButton,
    Stack,
    StackDivider
} from '@chakra-ui/react'
import { MdExpandMore } from "react-icons/md";

const Replies = ({ post_id }) => {
    const [ replies, setReplies ] = useState([]);
    
    const router = useRouter();

    const fetchReplies = async () => {
        const endpointUrl= process.env.NEXT_PUBLIC_BACKEND_ENDPOINT_URL
        const res = await fetch(`${endpointUrl}/replies/${post_id}`)
        if(res.ok){
            const data = await res.json();
            setReplies(data);
        }
    }

    useEffect(() => {
        fetchReplies()
    }, [])

    const redirectToDetail = (post_id) => {
        router.push(`/post/${post_id}`);
    }

    return (
        <>
        <Box maxH="500px" overflowY="auto"> 
            <Stack divider={<StackDivider />} spacing='4'>
                {replies.map((item) => (
                    <Card width="500px" key={item.id} mt="2" bgColor="gray.100">
                            <CardBody>
                                <Flex alignItems="center">
                                    <Avatar />
                                    <Box ml={3}>
                                        <Text fontSize='md'>
                                            {item.user_name}
                                        </Text>
                                        <Text fontSize='xs'>
                                            {item.created_at}
                                        </Text>
                                    </Box>
                                </Flex>
                                <Text mt='4' fontSize='md'>
                                    {item.text}
                                </Text>
                                <Flex 
                                    justifyContent="flex-end" 
                                    alignItems="flex-end"
                                    style={{ position: 'absolute', bottom: '10px', right: '10px' }}
                                >
                                    <IconButton 
                                        icon={<MdExpandMore/>}
                                        aria-label="Comment Button"
                                        onClick={() => redirectToDetail(item.id)}
                                        size="sm"
                                    />
                                </Flex>
                            </CardBody>
                    </Card>
                ))}
            </Stack>
        </Box>
        </>
    )
}

export default Replies;