"use client";

import { useEffect, useState } from "react"
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
} from '@chakra-ui/react'

    const PostIndex = () => {
        const [post, setPost] = useState([]);
    const fetchPost = async () => {
            try {
                const res = await fetch("http://localhost:8000/post", {
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

    return (
        <>
            <Card>
            <CardHeader>
                <Heading size='md'>ポスト一覧</Heading>
            </CardHeader>

            <CardBody>
                <Stack divider={<StackDivider />} spacing='4'>
                    {post.map((item) => (
                        <Box key={item.id}>
                            <Text pt='2' fontSize='md'>
                                {item.text}
                            </Text>
                            <Text fontSize='xs'>
                                {item.created_at}
                            </Text>
                        </Box>
                    ))}
                </Stack>
            </CardBody>
            </Card>
        </>
    )
}

export default PostIndex;
