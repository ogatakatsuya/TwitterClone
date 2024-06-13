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
    Link,
} from '@chakra-ui/react'
import { MdExpandMore } from "react-icons/md";
import PostButton from "./PostButton";

const PostIndex = () => {
    const router = useRouter();
    const [post, setPost] = useState([]);
    const [hasMore, setHasMore] = useState(true);
    const [offset, setOffset] = useState(0);
    const observerTarget = useRef(null);

    const fetchPost = async (offset) => {
        try {
            const endpointUrl = process.env.NEXT_PUBLIC_BACKEND_ENDPOINT_URL;
            const fetchLimit = 10
            const res = await fetch(`${endpointUrl}/posts?offset=${offset}&limit=${fetchLimit}`, {
                method: "GET",
            });
            if (res.ok) {
                const data = await res.json();
                if (offset == 0) { //初回表示時はレンダリングが2回行われるため
                    setPost(data);
                    setOffset(0);
                    console.log(data)
                } else {
                    setPost((prevPosts) => [...prevPosts, ...data]);
                    console.log(data)
                }
                setHasMore( data.length == fetchLimit )
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

    const formatDate = (date) => {
        const year = date.getFullYear();
        const month = ('0' + (date.getMonth() + 1)).slice(-2);
        const day = ('0' + date.getDate()).slice(-2);
        const hours = ('0' + date.getHours()).slice(-2);
        const minutes = ('0' + date.getMinutes()).slice(-2);
        return `${year}/${month}/${day} ${hours}:${minutes}`;
    };

    return (
        <>
            <Box maxH="680px" overflowY="auto">
                <Stack divider={<StackDivider />} spacing='4'>
                    {post.map((item) => (
                        <Card width="500px" key={item.id} bgColor="gray.100">
                            <CardBody>
                                <Flex alignItems="center">
                                    <Link href={`/profile/${item.user_id}`}><Avatar /></Link>
                                    <Box ml={3}>
                                        <Text fontSize='md'>
                                            {item.user_name}
                                        </Text>
                                        <Text fontSize='xs'>
                                            {formatDate(new Date(item.created_at))}
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
            <PostButton setPost={setPost}/>
        </>
    );
}

export default PostIndex;
