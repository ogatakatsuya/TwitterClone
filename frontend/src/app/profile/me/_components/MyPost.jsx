"use client";

import { useEffect, useState, useRef } from "react";
import Image from "next/image";
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
} from '@chakra-ui/react';
import { MdExpandMore } from "react-icons/md";

const MyPost = () => {
    const router = useRouter();
    const [post, setPost] = useState([]);
    const [hasMore, setHasMore] = useState(true);
    const [offset, setOffset] = useState(0);
    const [initialLoad, setInitialLoad] = useState(true); // 初回ロードフラグ
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
                if (offset === 0 && initialLoad) { // 初回表示時は上書きする
                    setPost(data);
                    setInitialLoad(false); // 初回ロードを完了としてマーク
                } else {
                    setPost((prevPosts) => [...prevPosts, ...data]);
                }
                setHasMore(data.length === 10);
            } else {
                console.error("Error fetching posts:", res.statusText);
            }
        } catch (error) {
            console.error("Error fetching posts:", error);
        }
    };

    useEffect(() => {
        if (hasMore && offset > 0) {
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
    };

    return (
        <>
            <Box maxH="680px" overflowY="auto">
                <Stack divider={<StackDivider />} spacing='4'>
                    {post.map((item) => (
                        <Card width="650px" key={item.id} bgColor="gray.100">
                            <CardBody>
                                <Flex alignItems="center">
                                    <Avatar src={item?.icon_url} />
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
                                    {item.file_url &&
                                        <Image
                                            src={item.file_url}
                                            width={200}
                                            height={200}
                                            alt="Image"
                                            style={{ width: 'auto', height: 'auto' }}
                                            priority
                                        />
                                    }
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
};

export default MyPost;
