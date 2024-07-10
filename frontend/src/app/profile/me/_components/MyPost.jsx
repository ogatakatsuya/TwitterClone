"use client";

import { useEffect, useState, useRef } from "react";
import { useRouter } from "next/navigation";
import {
    Card,
    CardBody,
    Text,
    Box,
    Avatar,
    Flex,
    IconButton,
    StackDivider,
    Stack,
} from '@chakra-ui/react'
import { MdExpandMore } from "react-icons/md";

const MyPost = () => {
    const router = useRouter();
    const [post, setPost] = useState([]);
    const [hasMore, setHasMore] = useState(true);
    const [offset, setOffset] = useState(0);
    const observerTarget = useRef(null);

    const fetchPost = async (offset) => {
        try {
            const endpointUrl = process.env.NEXT_PUBLIC_BACKEND_ENDPOINT_URL;
            const res = await fetch(`${endpointUrl}/profile/post/?offset=${offset}`, {
                method: "GET",
                credentials: "include",
            });
            if (res.ok) {
                const data = await res.json();
                if (offset === 0) { //初回表示時はレンダリングが2回行われるため
                    setPost(data);
                    setOffset(0);
                    console.log(data)
                } else {
                    setPost((prevPosts) => [...prevPosts, ...data]);
                    console.log(data)
                }
                setHasMore( data.length === 10 )
            } else {
                console.error("Error fetching posts:", res.statusText);
            }
        } catch (error) {
            console.error("Error fetching posts:", error);
        }
    };

    useEffect(() => {
        fetchPost(offset)
    },[])
    
    useEffect(() => {
        if (hasMore && offset>0) {
            console.log("fetch post")
            fetchPost(offset);
        }
    }, [offset, hasMore]);

    useEffect(() => {
        const observer = new IntersectionObserver(
            (entries) => {
                if (entries[0].isIntersecting && hasMore) {
                    setOffset((prev) => prev + 10);
                }
            },
            { threshold: 1.0 }
        );

        if (observerTarget.current) {
            observer.observe(observerTarget.current);
        }
        return () => {
            if (observerTarget.current) {
                observer.unobserve(observerTarget.current);
            }
        };
    }, [hasMore, observerTarget]);

    const redirectToDetail = (post_id) => {
        router.push(`/post/${post_id}`);
    }

    return (
        <>
            <Box maxH="680px" overflowY="auto">
                <Stack divider={<StackDivider />} spacing='4'>
                    {post.map((item) => (
                        <Card width="650px" key={item.id} bgColor="gray.100">
                            <CardBody>
                                <Flex alignItems="center">
                                    <Avatar src={item?.icon_url}/>
                                    <Box ml={3}>
                                        <Text fontSize='md'>
                                            {item.user_nickname ? item.user_nickname : item.user_name}
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
                                        icon={<MdExpandMore />}
                                        aria-label="Comment Button"
                                        onClick={() => redirectToDetail(item.id)}
                                        size="sm"
                                    />
                                </Flex>
                            </CardBody>
                        </Card>
                    ))}
                </Stack>
                <div ref={observerTarget} style={{ height: '20px' }}>
                    {/* ここでロード */}
                </div>
            </Box>
        </>
    );
}

export default MyPost;