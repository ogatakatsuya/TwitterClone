"use client";

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation";
import { 
    Card, 
    CardHeader, 
    CardBody, 
    CardFooter ,
    Stack,
    Text,
    StackDivider,
    Box,
    Heading,
    Avatar,
    Flex,
    IconButton,
    useDisclosure,
} from '@chakra-ui/react'
import { MdExpandMore } from "react-icons/md";

const PostIndex = () => {
    const router = useRouter();
    const [post, setPost] = useState([]);
    const fetchPost = async () => {
        try {
            const endpointUrl= process.env.NEXT_PUBLIC_BACKEND_ENDPOINT_URL
            const res = await fetch(`${endpointUrl}/posts?offset=${0}`, {
                method: "GET",
            });
            if (res.ok) {
                const data = await res.json();
                setPost(data);
                console.log(data); // データをログに出力する
            } else {
                console.error("Error fetching posts:", res.statusText);
            }
        } catch (error) {
            console.error("Error fetching posts:", error);
        }
    }
    
    useEffect(() => {
        fetchPost();
    },[])

    const redirectToDetail = (post_id) => {
        router.push(`/post/${post_id}`)
    }

    return (
        <>
        <Box maxH="680px" overflowY="auto">
            <Stack divider={<StackDivider />} spacing='4'>
                {post.map((item) => (
                    <Card width="500px" key={item.id}>
                        <CardBody>
                            <Flex alignItems="center">
                                <Avatar />
                                <Box ml={3}>
                                    <Text fontSize='md'>
                                        John Doe
                                    </Text>
                                    <Text fontSize='xs'>
                                        {item.created_at}
                                    </Text>
                                </Box>
                            </Flex>
                            <Box key={item.id}>
                                <Text mt='4' fontSize='md'>
                                    {item.text}
                                </Text>
                            </Box>
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

export default PostIndex;
