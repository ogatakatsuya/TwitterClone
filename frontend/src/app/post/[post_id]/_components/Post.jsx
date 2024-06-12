"use client";

import { useState, useEffect } from 'react'
import { 
    Card,
    CardBody,
    Text,
    Box,
    Avatar,
    Flex,
    IconButton,
    useDisclosure,
} from '@chakra-ui/react'
import { FaRegCommentDots } from "react-icons/fa";
import CommentModal from './ReplyModal';
import LikeButton from './LikeButton';

const Post = ({ post_id }) => {
    const [ post, setPost ] = useState("");
    const { isOpen, onOpen, onClose } = useDisclosure()
    
    const fetchPost = async () => {
        const endpointUrl= process.env.NEXT_PUBLIC_BACKEND_ENDPOINT_URL
        const res = await fetch(`${endpointUrl}/post/${post_id}`)
        if(res.ok){
            const data = await res.json();
            console.log(data)
            setPost(data);
        }
    }

    useEffect(() => {
        fetchPost();
    }, [])
    return (
        <>
            <Card width="500px" bgColor="gray.100">
                <CardBody>
                    <Flex alignItems="center">
                        <Avatar />
                        <Box ml={3}>
                            <Text fontSize='md'>
                                {post.user_name}
                            </Text>
                            <Text fontSize='xs'>
                                {post.created_at}
                            </Text>
                        </Box>
                    </Flex>
                    <Box>
                        <Text mt='4' fontSize='md'>
                            {post.text}
                        </Text>
                    </Box>
                    <Flex 
                        justifyContent="flex-end" 
                        alignItems="flex-end"
                        style={{ position: 'absolute', bottom: '10px', right: '10px' }}
                    >
                        <LikeButton post_id={post_id}/>
                        <IconButton 
                            icon={<FaRegCommentDots />}
                            aria-label="Comment Button"
                            onClick={onOpen}
                            size="sm"
                        />
                    </Flex>
                </CardBody>
            </Card>
            <CommentModal onClose={onClose} isOpen={isOpen} post_id={post_id}/>
        </>
    )
}

export default Post;